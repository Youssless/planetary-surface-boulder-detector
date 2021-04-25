class ImageFileState {
  String path;
  List<int>? size;

  ImageFileState.fetch({required this.path});
  
  ImageFileState({
      required this.path,
      required this.size
    });
}