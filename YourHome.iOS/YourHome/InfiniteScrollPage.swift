//
//  InfiniteScrollPage.swift
//  YourHome
//
//  Created by Frankie Lin on 9/21/25.
//

import SwiftUI

struct InfiniteScrollPage: View {
    @State var clicked: Bool = false
    @State var recommendations: APIManager.ImageIDData
    let user: APIManager.AuthData
    
    // State to manage the current page and drag gesture
    @State private var currentIndex: Int = 0
    @State private var dragOffset: CGFloat = .zero

    var body: some View {
        GeometryReader { proxy in
            // The height and width of each page will be the full screen size
            let pageHeight = proxy.size.height
            let pageWidth = proxy.size.width

            VStack(spacing: 0) {
                // We use indices here to easily check our position for loading more data
                ForEach(recommendations.image_ids.indices, id: \.self) { index in
                    let imageID = recommendations.image_ids[index]
                    
                    // A ZStack is used as a container for each page.
                    // This allows us to center the ImagePage content within the full-height page view.
                    ZStack {
                        ImagePage(id: imageID)
                    }
                    // Explicitly set the width and height for each page container
                    .frame(width: pageWidth, height: pageHeight) // Ensure each page container is full screen
                    .onAppear {
                        // When a page appears, check if we need to load more data
                        if shouldLoadMoreData(currentItemIndex: index) {
                            Task {
                                await updateRecommendations()
                            }
                        }
                    }
                }
            }
            // Explicitly set the width on the VStack to prevent it from shrinking
            .frame(width: pageWidth, height: pageHeight, alignment: .top)
            // 1. This offset positions the VStack to show the current page
            .offset(y: -CGFloat(currentIndex) * pageHeight)
            // 2. This offset provides the real-time "dragging" effect
            .offset(y: dragOffset)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        // Update the drag offset as the user's finger moves
                        dragOffset = value.translation.height
                    }
                    .onEnded { value in
                        // After the gesture ends, decide whether to switch pages
                        let swipeThreshold = pageHeight / 4
                        
                        if value.predictedEndTranslation.height < -swipeThreshold, currentIndex < recommendations.image_ids.count - 1 {
                            // Swiped up: Go to the next page
                            currentIndex += 1
                        } else if value.predictedEndTranslation.height > swipeThreshold, currentIndex > 0 {
                            // Swiped down: Go to the previous page
                            currentIndex -= 1
                        }
                        
                        // Animate the transition back to a stable state
                        withAnimation(.interactiveSpring()) {
                            dragOffset = .zero
                        }
                    }
            )
            .simultaneousGesture(
                DragGesture()
                    .onChanged { value in
                        if value.translation.width > 400 || value.translation.width < 400 {
                            Task {
                                await APIManager.like_image(userID: user.id, imageID: recommendations.image_ids[currentIndex])
                                currentIndex += 1
                            }
                        }
                    }
                )
        }
        .clipped() // Prevents views from appearing outside the GeometryReader frame
        .ignoresSafeArea() // Makes the view full-screen
        .onAppear {
            Task {
                // Load initial data if the list is empty
                if recommendations.image_ids.isEmpty {
                    await updateRecommendations()
                }
            }
        }
        Button(action: {
            Task {
                clicked = true
            }
        }) {
            if clicked {
                ProgressView()
            } else {
                Text("Personalized Room")
                    .fontWeight(.semibold)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
        .padding(.top, 10)
            NavigationLink(
                destination: FavoriteView(recs: recommendations, user: user),
                isActive: $clicked
            ) {
                EmptyView()
            }
        }
    

    /// Checks if the currently visible item is near the end of the list.
    private func shouldLoadMoreData(currentItemIndex index: Int) -> Bool {
        // Load new data when the user is 5 items away from the end of the current list
        let threshold = 5
        return (recommendations.image_ids.count - index) <= threshold
    }
    
    /// Fetches new recommendations and appends them to the list for a continuous scroll.
    private func updateRecommendations() async {
        let newRecs = await APIManager.get_rec(userID: user.id)
        // Append new items instead of replacing the whole list
        recommendations.image_ids.append(contentsOf: newRecs.image_ids)
    }
}


