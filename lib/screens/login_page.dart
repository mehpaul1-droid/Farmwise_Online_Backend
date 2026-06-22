import 'package:flutter/material.dart';
import '../core/auth_api.dart';
import 'register_page.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {

  final phone = TextEditingController();
  final password = TextEditingController();
  bool loading = false;

  void doLogin() async {
    setState(() => loading = true);

    final ok = await AuthApi.login(phone.text, password.text);

    setState(() => loading = false);

    if (ok) {
      Navigator.pushReplacementNamed(context, "/dashboard");
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("ورود ناموفق ❌")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [

            const Text(
              "سامانه هوشمند مدیریت فارم",
              style: TextStyle(color: Colors.white, fontSize: 20),
            ),

            const SizedBox(height: 30),

            TextField(
              controller: phone,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: "شماره موبایل",
                labelStyle: TextStyle(color: Colors.white70),
              ),
            ),

            TextField(
              controller: password,
              obscureText: true,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: "رمز عبور",
                labelStyle: TextStyle(color: Colors.white70),
              ),
            ),

            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: loading ? null : doLogin,
              child: Text(loading ? "در حال ورود..." : "ورود"),
            ),

            TextButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const RegisterPage(),
                  ),
                );
              },
              child: const Text("ثبت نام"),
            ),
          ],
        ),
      ),
    );
  }
}
