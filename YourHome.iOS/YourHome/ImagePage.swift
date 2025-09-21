//
//  ImagePage.swift
//  YourHome
//
//  Created by Frankie Lin on 9/20/25.
//

import SwiftUI
import Kingfisher

struct ImagePage: View {
    let id : Int
    var image: some View {
        KFImage(APIManager.get_img(imageID: id))
    }
    
    var body: some View {
        image.fixedSize(horizontal: false, vertical: false)
    }
}

#Preview {
    ImagePage(id: 1)
}
