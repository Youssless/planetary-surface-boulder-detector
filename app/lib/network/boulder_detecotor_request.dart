import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:app/model/boulder_list.dart';



Future<BoulderList> fetchBoulderList(Map<String, String> parameters) async {
  String url = "127.0.0.1:5000";
  String path = "/predict";
  
  final response = await http.get(Uri.http(url, path, parameters));
  print(response.statusCode);
  
  if (response.statusCode == 200) {
    print("${response.statusCode}");
    return BoulderList.fromJson(jsonDecode(response.body));
  }
  else {
    throw Exception("Failed to get boulder list ${response.statusCode}");
  }
}