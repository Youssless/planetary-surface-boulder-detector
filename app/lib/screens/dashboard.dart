import 'package:app/bloc/file/file_cubit.dart';
import 'package:app/bloc/file/file_state.dart';
import 'package:flutter/material.dart';
import 'package:app/widgets/side_navbar.dart';
import 'package:flutter/scheduler.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'dart:io';

import 'package:app/model/boulder_list.dart';
import 'package:app/bloc/network/network_cubit.dart';
import 'package:app/network/boulder_detecotor_request.dart';
import 'package:app/widgets/divider.dart';

class Home extends StatefulWidget {

  @override
  _Home createState() => new _Home();
}

class _Home extends State<Home> {
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
  }

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
  bool _isAwatingResult = false;

  TextEditingController _pathController = new TextEditingController();
  TextEditingController _widthController = new TextEditingController();
  TextEditingController _heightController = new TextEditingController();
  TextEditingController _sxController = new TextEditingController();
  TextEditingController _szController = new TextEditingController();
  TextEditingController _blPathController = new TextEditingController();

  @override
  void initState() {
    super.initState();
    
  }

  @override
  Widget build(BuildContext context) {

    return new Container(
      alignment: Alignment.centerLeft,
      padding: EdgeInsets.all(20),
      child: new LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
          return new Container(
            width: constraints.maxWidth,
            decoration: BoxDecoration(
              color: Colors.grey[100],
              borderRadius: BorderRadius.all(Radius.circular(25)) 
            ), 
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                Spacer(flex: 3,),
                Text(
                  "Dashboard"
                ),
                Spacer(flex: 3,),

                TextDivider(
                  text: "Processor target", 
                  indent: constraints.maxWidth*0.025
                ),

                // PROCESSOR FIELD
                  SizedBox(
                    width: constraints.maxWidth*0.9,
                    child: DropdownButtonFormField(
                      value: _value,
                      hint: Text("Processor"),
                      decoration: InputDecoration(
                        border: InputBorder.none
                      ),
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
                TextDivider(
                  text: "Image fields", 
                  indent: constraints.maxWidth*0.025
                ),

                // IMAGE SECTION
                BlocConsumer<ImageFileCubit, ImageFileState>(
                  listener: (BuildContext context, ImageFileState state) {
                    _pathController.text = state.path;
                    _widthController.text = state.size![0].toString();
                    _heightController.text = state.size![1].toString();
                  },
                  builder: (BuildContext context, ImageFileState state) {
                    return new SizedBox(
                      width: constraints.maxWidth*0.9,
                        child: TextFormField(
                          controller: _pathController,
                          readOnly: true,
                          decoration: InputDecoration(
                            border: InputBorder.none,
                            hintText: 'Input image path',
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
                              border: InputBorder.none,
                              hintText: 'Image width (Pixels)',
                            ),
                          ),
                        ),
                        SizedBox(
                          width: constraints.maxWidth*0.45,
                          child: TextFormField(
                            controller: _heightController,
                            decoration: InputDecoration(
                              border: InputBorder.none,
                              hintText: 'Image height (Pixels)',
                            ),
                          ),
                        ),
                      ],
                    );
                  }
                ),
                Spacer(flex: 2,),

                TextDivider(
                  text: "Surface model size", 
                  indent: constraints.maxWidth*0.025
                ),

                // SURFACE MODEL SECTION
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: constraints.maxWidth*0.45,
                      child: TextFormField(
                        controller: _sxController,
                        decoration: InputDecoration(
                          border: InputBorder.none,
                          hintText: 'DEM width (meters)',
                        ),
                      ),
                    ),
                    SizedBox(
                      width: constraints.maxWidth*0.45, 
                      child: TextFormField(
                        controller: _szController,
                        decoration: InputDecoration(
                          border: InputBorder.none,
                          hintText: 'DEM height (meters)',

                        ),
                      ),
                    ),
                  ],
                ),
                Spacer(flex: 3,),

                
                TextDivider(
                  text: "Boulderlist save location", 
                  indent: constraints.maxWidth*0.025
                ),

                //BOULDER LIST FILE LOCATION SECTION
                BlocConsumer<BLFileCubit, BLFileState>(
                  listener: (BuildContext context, BLFileState state) {
                    _blPathController.text = state.path;
                  },
                  builder: (BuildContext context, BLFileState state) {
                    return new SizedBox(
                      width: constraints.maxWidth*0.9,
                        child: TextFormField(
                          controller: _blPathController,
                          readOnly: true,
                          decoration: InputDecoration(
                            border: InputBorder.none,
                            hintText: 'Boulder list output directory',
                            suffixIcon: IconButton(
                              icon: Icon(Icons.folder),
                              onPressed: () {
                                BlocProvider.of<BLFileCubit>(context).open();
                              },
                            )
                          ),
                        )
                      );
                  },
                ),
                Spacer(flex: 2,),
                
                Divider(
                  height: 1,
                  indent: constraints.maxWidth*0.025,
                  endIndent: constraints.maxWidth*0.025,
                  thickness: 1,
                ),
                

                // RUN BUTTON
                SizedBox(
                  width: constraints.maxWidth*0.9,
                  height: 50,
                  child: ElevatedButton(
                    
                    onPressed: () {
                      BlocProvider.of<RequestCubit>(context).fetchBoulderList(
                        {
                          "processor": "cpu",
                          "imgs": _pathController.text,
                          "image_size": _widthController.text,
                          "surface_x": _sxController.text,
                          "surface_z": _szController.text,
                          "bl_out_file": _blPathController.text
                        }
                      ). then((value) {
                        BlocProvider.of<ImageFileCubit>(context).fetch(BlocProvider.of<RequestCubit>(context).state.outImagePath);
                      });
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
            )
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
      builder: (BuildContext context, BoxConstraints constraints) {
        return DefaultTabController(
            length: 2,
            child: Scaffold(
              appBar: new PreferredSize(
                preferredSize: Size.fromHeight(kToolbarHeight),
                child: new Container(
                  height: 50.0,
                  child: new TabBar(
                    tabs: [
                      Tab(icon: Icon(Icons.image, color: Colors.blue,)),
                      Tab(icon: Icon(Icons.file_copy_sharp, color: Colors.blue,)),
                    ],
                  ),
                ),
              ),
              body: TabBarView(
                  children: [
                    BlocBuilder<ImageFileCubit, ImageFileState>(
                      builder: (context, state) {

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
                      },
                    ),
                    
                    BlocConsumer<RequestCubit, BoulderList>(
                      listener: (context, state) {
                        
                      },
                      builder: (context, state) {
                        return state.boulders.isNotEmpty ? 
                        new Container(
                          child: SingleChildScrollView(
                            child: Builder(
                              builder: (context) {
                                //List<int>? dem_size = BlocProvider.of<ImageFileCubit>(context).state.size;
                                String boulder_list  = """identifier PANGU: Boulder List File
horizontal_scale 1
offset 0 0
size 1200 1200

""";
                                for (var item in state.boulders) {
                                  for (List<dynamic> boulders in item) {
                                    boulder_list += boulders.join(" ") + "\n";
                                  }
                                }
                                //print(concatenate);
                                return Text(boulder_list);
                              }
                            )
                            
                            
                            ),
                        )
                        :
                        new Container(
                          alignment: Alignment.center,
                          child: Text("Nothing to display"),
                        );
                      }, 
                    ),
                    
                  ]
              )
            )
          );
      }
    );
  }
}
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