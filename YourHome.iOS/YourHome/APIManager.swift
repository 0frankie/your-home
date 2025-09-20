import Foundation

class APIManager {
    
    // Singleton pattern (optional, but can be useful)
    static let shared = APIManager()
    
    private init() {}
    
    // Function to make POST request
    func postData(url: String, parameters: [String : String]) async -> Bool {
        guard let url_Processed = URL(string: url) else { return false}
        
        var request = URLRequest(url: url_Processed)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("true", forHTTPHeaderField: "ngrok-skip-browser-warning")
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters)
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status code: \(httpResponse.statusCode)")
                
                if (200...299).contains(httpResponse.statusCode) {
                    // Success
                    if let json = try? JSONSerialization.jsonObject(with: data) {
                        print(json)
                        return true
                    }
                } else {
                    // Error from server
                    print("Request failed with status code: \(httpResponse.statusCode)")
                    return false
                }
            }
        } catch {
            print("Request error: \(error.localizedDescription)")
        }
        return false
    }
}

func login(baseurlData: String, username: String, password: String) async -> Bool {
    let PARAMETERS = ["username": username, "password": password] // Replace with actual parameters you need to send
    let authenticateUrl = baseurlData + "/api/authenticate"
    return await APIManager.shared.postData(url: authenticateUrl, parameters: PARAMETERS)
}
