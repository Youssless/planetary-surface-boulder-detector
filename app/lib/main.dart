import 'package:flutter/material.dart';
import 'screens/dashboard.dart';
import 'util/theme.dart';
import 'dart:io';

void main() {
  // Process.start("start", ["..\\server.bat"], runInShell: true)
  //   .then((value) => {
  //     stdout.write(value.stdout),
  //     stderr.write(value.stderr)
  //   });
  runApp(PlanetaryBoulderDetector());
}


class PlanetaryBoulderDetector extends StatefulWidget {

  @override
  _PlanetaryBoulderDetector createState() => new _PlanetaryBoulderDetector();
}

class _PlanetaryBoulderDetector extends State<PlanetaryBoulderDetector> {

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Planetary Boulder Detector',
      theme: DefaultTheme,
      home: Home(),
    );
  }
}