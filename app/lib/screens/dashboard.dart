import 'package:app/bloc/file/file_cubit.dart';
import 'package:app/bloc/file/file_state.dart';
import 'package:flutter/material.dart';
import 'package:app/widgets/side_navbar.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'dart:io';

class Home extends StatefulWidget {

  @override
  _Home createState() => new _Home();

}

class _Home extends State<Home> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      body: new Container(
        child: Row (
          children: [
            Expanded(
              flex: 2,
              child: SideNavbar(),
            ),
            Expanded(
              flex: 10,
              child: Dashboard()
            ),
            Expanded(
              flex: 20,
              child: ImageView()
            )
            
          ],
        ),
      )
    );
  }
}


class Dashboard extends StatefulWidget {

  @override
  _Dashboard createState() => new _Dashboard();
}

class _Dashboard extends State<Dashboard> {
  int? _value = 0;
  String _path = "";

  TextEditingController _pathController = new TextEditingController();
  TextEditingController _widthController = new TextEditingController();
  TextEditingController _heightController = new TextEditingController();


  @override
  Widget build(BuildContext context) {

    return new Container(
      alignment: Alignment.centerLeft,
      padding: EdgeInsets.all(20),
      child: new LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          return new Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Text(
                "Dashboard"
              ),
              Spacer(flex: 6,),
              Text(
                "Processing"
              ),
              SizedBox(
                width: constraints.maxWidth*0.9,
                child: DropdownButtonFormField(
                  value: _value,
                  hint: Text("Processor"),
                  items: [
                    DropdownMenuItem(
                      child: Text("CPU"),
                      value: 0,
                    ),
                    DropdownMenuItem(
                      child: Text(
                        "GPU",
                        style: TextStyle(color: Colors.grey),
                      ),
                      value: 1,
                      onTap: null
                    )
                  ],
                  onChanged: null
                )
              ),
              Spacer(flex: 2,),
              Text(
                "Input Image"
              ),
              BlocConsumer<ImageFileCubit, ImageFileState>(
                listener: (BuildContext context, ImageFileState state) {
                  _pathController.text = state.path;
                  _widthController.text = state.size[0].toString();
                  _heightController.text = state.size[1].toString();
                },
                builder: (BuildContext context, ImageFileState state) {
                  return new SizedBox(
                    width: constraints.maxWidth*0.9,
                      child: TextFormField(
                        controller: _pathController,
                        readOnly: true,
                        decoration: InputDecoration(
                          //border: InputBorder.none,
                          hintText: 'Image path',
                          suffixIcon: IconButton(
                            icon: Icon(Icons.folder),
                            onPressed: () {
                              BlocProvider.of<ImageFileCubit>(context).open();
                            },
                          )
                        ),
                      )
                    );
                },
              ),
              BlocBuilder<ImageFileCubit, ImageFileState>(
                builder: (BuildContext context, ImageFileState state) {
                  return new Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(
                        width: constraints.maxWidth*0.45,
                        child: TextFormField(
                          controller: _widthController,
                          decoration: InputDecoration(
                            //border: InputBorder.none,
                            hintText: 'width (meters)',
                          ),
                        ),
                      ),
                      SizedBox(
                        width: constraints.maxWidth*0.45,
                        child: TextFormField(
                          controller: _heightController,
                          decoration: InputDecoration(
                            //border: InputBorder.none,
                            hintText: 'height (meters)',
                          ),
                        ),
                      ),
                    ],
                  );
                }
              ),
              Spacer(flex: 2,),
              Text(
                "Surface Model"
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'width (pixels)',
                      ),
                    ),
                  ),
                  SizedBox(
                    width: constraints.maxWidth*0.45,
                    child: TextFormField(
                      decoration: InputDecoration(
                        //border: InputBorder.none,
                        hintText: 'height (pixels)',
                      ),
                    ),
                  ),
                ],
              ),
              Spacer(flex: 3,),
              SizedBox(
                width: constraints.maxWidth*0.9,
                height: 50,
                child: ElevatedButton(
                  onPressed: () {
                    
                  }, 
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text("Run")
                    ],
                  )
                ),
              ),
              Spacer(flex: 12,)
            ],
          );
        },
      )
    );
  }
}

class ImageView extends StatefulWidget {

  @override
  _ImageView createState() => new _ImageView();
}

class _ImageView extends State<ImageView> {

  @override
  Widget build(BuildContext context) {
    return new LayoutBuilder(
      builder: (BuildContext context, BoxConstraints constraints) 
        => BlocBuilder<ImageFileCubit, ImageFileState>(
          builder: (BuildContext context, ImageFileState state) {
            return state.path.isNotEmpty ? 
              new Container(
                alignment: Alignment.center,
                constraints: BoxConstraints(
                  maxHeight: constraints.maxHeight*0.95,
                  maxWidth: constraints.maxWidth,
                ),
                decoration: BoxDecoration(
                  image: DecorationImage(
                    image: FileImage(File(state.path)),
                    fit: BoxFit.contain
                  )
                ),
              )
              :
              new Container(
                alignment: Alignment.center,
                child: Text("Nothing to display"),
              );
          }
        )
    );
    //   child: new Row(
    //     mainAxisAlignment: MainAxisAlignment.center,
    //     children: [
    //       BlocBuilder<FileCubit, FileState>(
    //         builder: (BuildContext context, FileState state) {
    //           return state.path.isNotEmpty ?
    //             Image.file(
    //                 File(state.path),
    //                 fit: BoxFit.cover,
    //               )
    //             :
    //             new Container(
    //               child: Text("Nothing to display"),
    //             );
    //         }
    //       )
    //     ],
    //   ),
    // );
  }
}