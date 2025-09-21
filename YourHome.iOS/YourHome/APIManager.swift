import Foundation

internal class APIManager {
    
    // Singleton pattern (optional, but can be useful)
    static let shared = APIManager()
    
    private init() {}
    
    struct AuthData : Codable {
        var device_id: String
        var email: String
        var id: Int
        var username: String
        
        static func emptyAuthData() -> AuthData {
            .init(device_id: "", email: "", id: -1, username: "")
        }
        
        static func == (lhs: APIManager.AuthData, rhs: APIManager.AuthData) -> Bool {
            return lhs.device_id == rhs.device_id && lhs.email == rhs.device_id && lhs.id == rhs.id && lhs.username == rhs.username
        }
    }
    
    
    
    // Function to make POST request
    func postData(url: String, parameters: [String : String]) async -> AuthData {
        let empty = AuthData.emptyAuthData()
        guard let url_Processed = URL(string: url) else { return empty }
        
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
                    if let json = try? JSONSerialization.jsonObject(with: data) {
                        let decoder = JSONDecoder()
                        let parsed = try decoder.decode(AuthData.self, from: data)
                        return parsed
                    }
                } else {
                    // Error from server
                    print("Request failed with status code: \(httpResponse.statusCode)")
                    return empty
                }
            }
        } catch {
            print("Request error: \(error.localizedDescription)")
        }
        return empty
    }
    
    static internal func login(baseurlData: String, deviceID: String, username: String, password: String) async -> AuthData {
        let PARAMETERS = ["device_id": deviceID, "username": username, "password": password] // Replace with actual parameters you need to send
        let authenticateUrl = baseurlData + "/api/authenticate"
        return await APIManager.shared.postData(url: authenticateUrl, parameters: PARAMETERS)
    }
    
}

