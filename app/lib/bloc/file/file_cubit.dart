import 'package:app/bloc/file/file_state.dart';
import 'package:filepicker_windows/filepicker_windows.dart';
import 'package:bloc/bloc.dart';
import 'dart:io';

import 'package:flutter/cupertino.dart';

abstract class FileCubit<T> extends Cubit<T>{

  FileCubit(T initialState) : super(initialState);

  void open();
}

class ImageFileCubit extends FileCubit<ImageFileState> {

  ImageFileCubit() : super(ImageFileState(path: "", size: [0, 0]));

  void open() {
    final file = OpenFilePicker()
      ..filterSpecification = {
        "Image Files (*.jpg; *.jpeg; *.png)": "*.jpg;*.jpeg;*.png",
      }
      ..title = "Select an image";
     
    final result = file.getFile();
    
    if (result != null) {
      result.readAsBytes().then((value) { 
          // get the image width and height
          var decodedImg = decodeImageFromList(value);
          decodedImg.then(
            (value) {
              // send the data to the stream
              emit(ImageFileState(
                path: result.path,
                size: [value.width, value.height]
              ));
            }
          );
        }
      );
    }
  }

  void fetch(String path) {
    emit(ImageFileState.fetch(
      path: path,
      )
    );
  }
}

class BLFileState {
  String path;
  BLFileState({required this.path});
}

class BLFileCubit extends FileCubit<BLFileState> {
  BLFileCubit() : super(BLFileState(path: ""));

  void open() {
   final file =  SaveFilePicker()
    ..filterSpecification = {
      "Text Document (.txt)": ".*txt"
    }
    ..title = "Boulder list save location"
    ..defaultExtension = "txt";
   final result = file.getFile();

   if (result != null) {
     emit(BLFileState(path: result.path));
   }
  }
}