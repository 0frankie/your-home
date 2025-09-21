//
//  ImagePage.swift
//  YourHome
//
//  Created by Frankie Lin on 9/20/25.
//

import SwiftUI
import Kingfisher

struct ImagePage: View {
    let image = KFImage(URL(string: "https://electroluminescent-plagihedral-dane.ngrok-free.app/api/get-image-file/1"))
    
    var body: some View {
        let scale = UIScreen.main.scale
        let resizingProcessor = ResizingImageProcessor(referenceSize: CGSize(width: 1000.0 * scale, height: 1000.0 * scale), mode: .aspectFill)
        image.resizable().setProcessor(resizingProcessor)
    }
}

func rescaledImage(url: URL) {
    
}

#Preview {
    ImagePage()
}
