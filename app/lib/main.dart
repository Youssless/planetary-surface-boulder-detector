import 'package:app/bloc/file/file_cubit.dart';
import 'package:flutter/material.dart';
import 'screens/dashboard.dart';
import 'util/theme.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
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
    return MultiBlocProvider(
      providers: [
        BlocProvider<ImageFileCubit>(
          create: (context) => ImageFileCubit()
        )
      ], 
      child: MaterialApp(
        title: 'Planetary Boulder Detector',
        theme: DefaultTheme,
        home: Home(),
      )
    );
    
  }
}