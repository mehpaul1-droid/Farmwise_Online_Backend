import 'package:flutter/material.dart';
import '../core/auth_api.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {

  final phone = TextEditingController();
  final password = TextEditingController();
  bool loading = false;

  void doRegister() async {
    setState(() => loading = true);

    final ok = await AuthApi.register(phone.text, password.text);

    setState(() => loading = false);

    if (ok) {
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("ثبت نام ناموفق ❌")),
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
              "ثبت نام کارگر",
              style: TextStyle(color: Colors.white, fontSize: 20),
            ),

            const SizedBox(height: 20),

            TextField(
              controller: phone,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(labelText: "شماره موبایل"),
            ),

            TextField(
              controller: password,
              obscureText: true,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(labelText: "رمز عبور"),
            ),

            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: loading ? null : doRegister,
              child: Text(loading ? "در حال ثبت..." : "ثبت نام"),
            ),
          ],
        ),
      ),
    );
  }
}
