//
//  LoginView.swift
//  urhome
//
//  Created by Ming Zhang on 9/21/25.
//


import SwiftUI

struct LoginView: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var errorMessage: String = ""
    @State private var isLoading: Bool = false
    @State private var isLoggedIn: Bool = false
    @State private var json: APIManager.AuthData = APIManager.AuthData.empty()
    @State private var recs: APIManager.ImageIDData = APIManager.ImageIDData.empty()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Your Home")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding(.top, 100)
                
                Text("Swipe to your next dream")
                    .font(.subheadline)
                    .fontWeight(.ultraLight)
                    .padding(.bottom, 20)
                
                // Username field
                TextField("Enter username", text: $username)
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                    .autocapitalization(.none)
                
                // Password field
                SecureField("Enter password", text: $password)
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(10)
                
                // Error message
                if !errorMessage.isEmpty {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .font(.subheadline)
                }
                
                // Login button
                Button(action: {
                    Task {
                        json = await APIManager.login(deviceID: UIDevice.current.identifierForVendor!.uuidString, username: username, password: password)
                        recs = await APIManager.get_rec(userID: json.id)
                        isLoggedIn = !(json == APIManager.AuthData.empty())
                    }
                }) {
                    if isLoading {
                        ProgressView()
                    } else {
                        Text("Login")
                            .fontWeight(.semibold)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
                .padding(.top, 10)
                
                Spacer()
                
                // Navigate to next screen after login
                NavigationLink(
                    destination: InfiniteScrollPage(recommendations: recs, user: json),
                    isActive: $isLoggedIn
                ) {
                    EmptyView()
                }
            }
            .padding()
        }
    }
}

// Placeholder for the next screen
struct BedroomFinderView: View {
    var body: some View {
        Text("Welcome! Let’s find your dream bedroom :bed:")
            .font(.title2)
            .padding()
    }
}

#Preview {
    ContentView()
}
