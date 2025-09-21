import Foundation

internal class APIManager {
    
    // Singleton pattern (optional, but can be useful)
    static let shared = APIManager()
    
    private init() {}
    
    protocol Data : Codable {
        static func empty() -> Self
        
        static func == (lhs: Self, rhs: Self) -> Bool
    }
    
    enum RequestType : String {
        case authType = "auth"
        case recType =  "recommendations"
        case likeType = "likeImage"
        case imageType = "getImage"
    }
    
    struct AuthData : Data {
        var device_id: String
        var email: String
        var id: Int
        var username: String
        
        static func empty() -> AuthData {
            .init(device_id: "", email: "", id: -1, username: "")
        }
        
        static func == (lhs: APIManager.AuthData, rhs: APIManager.AuthData) -> Bool {
            return lhs.device_id == rhs.device_id && lhs.email == rhs.email && lhs.id == rhs.id && lhs.username == rhs.username
        }
    }
    
    struct ImageIDData : Data {
        
        var imageIDData: [Int]
        
        static func empty() -> ImageIDData {
            .init(imageIDData: [])
        }
        
        static func == (lhs: APIManager.ImageIDData, rhs: APIManager.ImageIDData) -> Bool {
            return lhs.imageIDData == rhs.imageIDData
        }
        
    }
    
    struct ImageLikedData : Data {
        var message: String
        
        static func empty() -> ImageLikedData {
            .init(message: "")
        }
        
        static func == (lhs: APIManager.ImageLikedData, rhs: APIManager.ImageLikedData) -> Bool {
            return lhs.message == rhs.message
        }
    }
    
    struct ImageFileData : Data {
        var file_link : String
        
        static func empty() -> ImageFileData {
            .init(file_link: "")
        }
        
        static func == (lhs: APIManager.ImageFileData, rhs: APIManager.ImageFileData) -> Bool {
            return lhs.file_link == rhs.file_link
        }
    }
    

    
    
    
    // Function to make POST request
    func postData(url: String, parameters: [String : String], requestType: RequestType) async -> any Data {
        let empty1 = AuthData.empty()
        let empty2 = ImageLikedData.empty()
        
        guard let url_Processed = URL(string: url) else { return empty1 }
        
        var request = URLRequest(url: url_Processed)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("true", forHTTPHeaderField: "ngrok-skip-browser-warning")
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters)
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status code: \(httpResponse.statusCode)")

                
                if (200...399).contains(httpResponse.statusCode) {
                    // Success
                    if requestType.self.rawValue == "auth" {
                        if let json = try? JSONSerialization.jsonObject(with: data) {
                            let decoder = JSONDecoder()
                            let parsed = try decoder.decode(AuthData.self, from: data)
                            return parsed
                        }
                    }
                   
                    if requestType.self.rawValue == "likeImage" {
                        if let json = try? JSONSerialization.jsonObject(with: data) {
                            let decoder = JSONDecoder()
                            let parsed = try decoder.decode(ImageLikedData.self, from: data)
                            return parsed
                        }
                    }

                } else {
                    // Error from server
                    print("Request failed with status code: \(httpResponse.statusCode)")
                    return empty1
                }
            }
        } catch {
            print("Request error: \(error.localizedDescription)")
        }
        return empty1
    }
    
    func getData(url: String, requestType: RequestType) async -> any Data {
        let empty1 = ImageIDData.empty()
        let empty2 = ImageFileData.empty()
        
        guard let url_Processed = URL(string: url) else { return empty1 }
        
        var request = URLRequest(url: url_Processed)
        request.httpMethod = "GET"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("true", forHTTPHeaderField: "ngrok-skip-browser-warning")
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status code: \(httpResponse.statusCode)")

                
                if (200...399).contains(httpResponse.statusCode) {
                    // Success
                    if requestType.self.rawValue == "recommendations" {
                        if let json = try? JSONSerialization.jsonObject(with: data) {
                            let decoder = JSONDecoder()
                            let parsed = try decoder.decode(ImageIDData.self, from: data)
                            return parsed
                        }
                    }
                   
                    if requestType.self.rawValue == "getImage" {
                        if let json = try? JSONSerialization.jsonObject(with: data) {
                            let decoder = JSONDecoder()
                            let parsed = try decoder.decode(ImageFileData.self, from: data)
                            return parsed
                        }
                    }

                } else {
                    // Error from server
                    print("Request failed with status code: \(httpResponse.statusCode)")
                    return empty1
                }
            }
        } catch {
            print("Request error: \(error.localizedDescription)")
        }
        return empty1
    }
    
    static internal func login(baseurlData: String, deviceID: String, username: String, password: String) async -> AuthData {
        let authenticateUrl = baseurlData + "/api/authenticate"
        let PARAMETERS = ["device_id": deviceID, "username": username, "password": password] // Replace with actual parameters you need to send
        return await APIManager.shared.postData(url: authenticateUrl, parameters: PARAMETERS, requestType: RequestType.authType) as! AuthData
    }
    
    
    static internal func get_rec(baseurlData: String, userID: String) async -> ImageIDData {
        let recUrl = baseurlData + "/get-user-recommendations/" + userID
        return await APIManager.shared.getData(url: recUrl, requestType: RequestType.recType) as! ImageIDData
    }
    
    
    static internal func like_image(baseurlData: String , userID: String, imageID: String) async -> ImageLikedData {
        let imageLikedUrl = baseurlData + "/api/like-image"
        let PARAMETERS = ["user_id": userID, "imageID": imageID]
        return await APIManager.shared.postData(url: imageLikedUrl, parameters: PARAMETERS, requestType: RequestType.imageType) as! APIManager.ImageLikedData
    }
    
    static internal func get_rec(baseurlData: String, userID: String) async -> ImageFileData {
        let getfileUrl = baseurlData + "/get-user-recommendations/" + userID
        return await APIManager.shared.getData(url: getfileUrl, requestType: RequestType.recType) as! ImageFileData
    }
    
}

