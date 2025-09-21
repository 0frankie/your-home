//
//  FavoriteView.swift
//  YourHome
//
//  Created by Frankie Lin on 9/21/25.
//

import SwiftUI
import Kingfisher

struct FavoriteView: View {
    @State var clicked: Bool = false
    var recs: APIManager.ImageIDData
    var user: APIManager.AuthData
    
    var body: some View {
        GeometryReader { proxy in
            // The height and width of each page will be the full screen size
            let pageHeight = proxy.size.height
            let pageWidth = proxy.size.width
            
            KFImage(APIManager.get_favorite(userID: 2))
                .frame(width: pageWidth, height: pageHeight)
                .onAppear {
                    Button(action: {
                        Task {
                            clicked = true
                        }
                    }) {
                        if clicked {
                            ProgressView()
                        } else {
                            Text("Return")
                                .fontWeight(.semibold)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                    }
                    .padding(.top, 10)
                    
                }
        }
        NavigationLink(
            destination: InfiniteScrollPage(recommendations: recs, user: user),
            isActive: $clicked
        ) {
            EmptyView()
        }
    }
}
