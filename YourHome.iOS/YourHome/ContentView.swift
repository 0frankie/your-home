//
//  ContentView.swift
//  YourHome
//
//  Created by Frankie Lin on 9/20/25.
//

import SwiftUI
import Kingfisher

struct ContentView: View {
    @State var loginResponse: APIManager.AuthData = APIManager.AuthData.empty()
    @State var likeResponse: APIManager.ImageLikedData =
        APIManager.ImageLikedData.empty()
    @State var IDResponse: APIManager.ImageIDData =
        APIManager.ImageIDData.empty()
    @State var fileResponse: APIManager.ImageFileData =
        APIManager.ImageFileData.empty()
    
    var body: some View {
        VStack {
            LoginView()
        }
        .padding()
        .onAppear {
            Task {
//                loginResponse = await APIManager.login(deviceID: UIDevice.current.identifierForVendor!.uuidString, username: "franklin", password: "password")
                
//                likeResponse = await APIManager.like_image(baseurlData: "https://electroluminescent-plagihedral-dane.ngrok-free.app/", userID: 1, imageID: 4)
//                IDResponse = await APIManager.get_rec(userID: 1)
            }
        }
    }
}

#Preview {
    ContentView()
}
