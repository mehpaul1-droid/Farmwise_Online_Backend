import 'package:flutter/material.dart';
import '../core/auth_service.dart';
import '../core/analytics_api.dart';
import '../widgets/profit_advanced_chart.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? analytics;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    load();
  }

  Future<void> load() async {
    try {
      final data = await AnalyticsApi.getProfitData();
      setState(() {
        analytics = data;
        loading = false;
      });
    } catch (e) {
      setState(() {
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final role = AuthService.role ?? "user";

    if (loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),

      appBar: AppBar(
        title: const Text("سامانه هوشمند فارم"),
        backgroundColor: const Color(0xFF1B5E20),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: load,
          ),
        ],
      ),

      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          ProfitAdvancedChart(data: analytics),

          const SizedBox(height: 20),

          _kpi("درآمد کل", _sum(analytics?["revenue"])),
          _kpi("هزینه کل", _sum(analytics?["cost"])),
          _kpi("سود کل", _sum(analytics?["profit"])),

          const SizedBox(height: 20),

          _section("وضعیت سیستم", "آنلاین 🟢"),

          if (role == "admin")
            _section("دسترسی", "مدیر کامل سیستم"),

          if (role == "user")
            _section("دسترسی", "کاربر عادی"),
        ],
      ),
    );
  }

  String _sum(List? list) {
    if (list == null) return "0";
    return list.fold(0.0, (a, b) => a + b).toString();
  }

  Widget _kpi(String t, String v) {
    return Card(
      color: const Color(0xFF111C33),
      child: ListTile(
        title: Text(t, style: const TextStyle(color: Colors.white70)),
        trailing: Text(v, style: const TextStyle(color: Colors.greenAccent)),
      ),
    );
  }

  Widget _section(String t, String v) {
    return Card(
      color: const Color(0xFF1E293B),
      child: ListTile(
        title: Text(t, style: const TextStyle(color: Colors.white70)),
        trailing: Text(v, style: const TextStyle(color: Colors.white)),
      ),
    );
  }
}
