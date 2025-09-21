//
//  ContentView.swift
//  YourHome
//
//  Created by Frankie Lin on 9/20/25.
//

import SwiftUI
import Kingfisher

struct ContentView: View {
    @State var loginResponse: APIManager.AuthData = APIManager.AuthData.emptyAuthData()
    
    var body: some View {
        VStack {
            
        }
        .padding()
        .onAppear {
            Task {
                loginResponse = await APIManager.login(baseurlData: "https://electroluminescent-plagihedral-dane.ngrok-free.app/", deviceID: UIDevice.current.identifierForVendor!.uuidString, username: "franklin", password: "password")
            }
        }
    }
}

#Preview {
    ContentView()
}
