import launch

if not launch.is_installed("opencv-contrib-python"):
    if launch.is_installed("opencv-python"):
        launch.run_pip("uninstall opencv-python")    
        print("Uninstalling opencv-python...")    
    launch.run_pip("install opencv-contrib-python")
    print("Installing opencv-contrib-python...")

if not launch.is_installed("numpy"):
    launch.run_pip("install numpy")
    print("Installing numpy...")
