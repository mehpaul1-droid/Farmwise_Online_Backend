import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthApi {

  static const String baseUrl =
      "https://farmwiseonlinebackend-production.up.railway.app";

  // ---------------- REGISTER ----------------
  static Future<bool> register(String phone, String password) async {
    final response = await http.post(
      Uri.parse("\$baseUrl/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "phone": phone,
        "password": password,
      }),
    );

    final data = jsonDecode(response.body);
    return data["status"] == "ok";
  }

  // ---------------- LOGIN ----------------
  static Future<bool> login(String phone, String password) async {
    final response = await http.post(
      Uri.parse("\$baseUrl/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "phone": phone,
        "password": password,
      }),
    );

    final data = jsonDecode(response.body);
    return data["status"] == "ok";
  }
}
