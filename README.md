# Team201
Repository for all of Low Cost Motion Capture Project code

Team 201 Prototyping Files:

In chronological order:

1. Hardware: MPU6050 (6-axis accelerometer, gyroscope) tested using example arduino programs from MPU libraries

2. Hardware: MPU9250 (9-axis, including magnetometer) tested using example arduino programs, as well as...
	-magnettest.ino, testing magnetometer output (dependencies: MPU9250 library)
	-twoimutest.ino, testing using two IMUs with one MCU (dependencies: MPU9250, Wire library)
	
	-imu_guitest.py, testing creating animation from IMU angles (.txt file inpput) in python script, UNSUCCESSFUL
	-secondanimationtest.py, ", SUCCESSFUL (created a dynamic animation that draws two lines based on .txt file input)

3. Hardware: BNO055 (9-axis accel/gyro/magn/ with sensor fusion, tested with library examples as well as...

	-bnotest.ino, testing printing multiple outputs of the BNO as well as interfacing multiple on the same MCU
	-matplottest.py, CURRENT FILE, tests extracting data straight to python from arduino, processes data using quaternion and rotation matrix math, creating a GUI that plots the values from each IMU

4. Hardware: MPU6050, 
	(moved back to less complex IMU for time-sensitive, proof of concept purposes)

	-ArmAngleTest.ino, tests the angles of multiple IMUS, just printed in serial monitor
	-Multi_IMU_Quat_Angle.ino, uses quaternion math to determine absolute angle, just printed in serial monitor
