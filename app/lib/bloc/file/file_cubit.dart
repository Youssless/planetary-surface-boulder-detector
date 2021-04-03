import 'package:app/bloc/file/file_state.dart';
import 'package:filepicker_windows/filepicker_windows.dart';
import 'package:bloc/bloc.dart';
import 'dart:io';

import 'package:flutter/cupertino.dart';

class ImageFileCubit extends Cubit<ImageFileState> {

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
}