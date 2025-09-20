//
//  ContentView.swift
//  YourHome
//
//  Created by Frankie Lin on 9/20/25.
//

import SwiftUI
import Kingfisher

struct ContentView: View {
    var body: some View {
        let deviceID = UIDevice.current.identifierForVendor!.uuidString
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
        }
        .padding()
        .onAppear {
            print(KingfisherManager.shared)
        }
    }
}

#Preview {
    ContentView()
}
