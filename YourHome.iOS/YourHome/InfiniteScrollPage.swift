//
//  InfiniteScrollPage.swift
//  YourHome
//
//  Created by Frankie Lin on 9/21/25.
//

import SwiftUI

struct InfiniteScrollPage: View {
    @State var recommendations: APIManager.ImageIDData
    let user: APIManager.AuthData
    var i: Int { 0 }
    
    
    var body: some View {
        if i <= recommendations.imageIDData.count / 2 {
            ImagePage(id: recommendations.imageIDData[i])
        } else {
//            InfiniteScrollPage(recommendations: APIManager.get_rec(userID: user.id), user: user)
            ImagePage(id: recommendations.imageIDData[i])
            updateRecommendations()
        }
    }
    func updateRecommendations() async {
        recommendations = await APIManager.get_rec(userID: user.id)
    }
}

#Preview {
    InfiniteScrollPage(recommendations: APIManager.ImageIDData.empty(), user: APIManager.AuthData.empty())
}
