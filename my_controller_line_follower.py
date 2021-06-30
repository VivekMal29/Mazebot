"""my_controller_line_follower controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor

from controller import Robot
import os

        
    
def run_robot(robot):
    
    
    #time in millisecs after which we want rerun the code
    time_step = 10
    
    
    
    max_speed = 6.48  #2*pi (to keep it simplified)
    arr = ""          #array to store the path
   
    
    write_flag = True  
    
    #decalring motor as devices
    
    
    
    
    left_motor = robot.getDevice('motor_1')
    right_motor= robot.getDevice('motor_2')
    
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)
  
    front_ir_left = robot.getDevice('ir_F_L')
    front_ir_left.enable(time_step)
    
    front_ir_right = robot.getDevice('ir_F_R')
    front_ir_right.enable(time_step)
    
    front_ir_mid = robot.getDevice('ir_F_M')
    front_ir_mid.enable(time_step)
    
    centre_ir = robot.getDevice('ir_0')
    centre_ir.enable(time_step)
    
    left_ir_1 = robot.getDevice('ir_L_1')
    left_ir_1.enable(time_step)
    
    left_ir_2 = robot.getDevice('ir_L_2')
    left_ir_2.enable(time_step)
    
    right_ir_1 = robot.getDevice('ir_R_1')
    right_ir_1.enable(time_step)
    
    right_ir_2 = robot.getDevice('ir_R_2')
    right_ir_2.enable(time_step)
    
    
    
    
    dead_end = 0             
    turning_right=0
    turning_left=0
    move_straight=0
    detected=0
    end_maze=0
    
    
    while robot.step(time_step)!=-1:
        print (arr)
        current_time = robot.getTime()
           
        left_speed = max_speed
        right_speed = max_speed
        
      
        if(end_maze==0 and dead_end==0 and turning_right==0 and turning_left==0):
                
                #minute error correction
                #if bot deviates from Line 
                if(right_ir_1.getValue()>400):                    
                    right_speed = -max_speed*0.2
                    
                elif(left_ir_1.getValue()>400):
                    left_speed = -max_speed*0.2
                    
                check_intersection=0  
                
                
                
                
                #no matter what you need to turn right when rightmost sensor detect black line
                if(right_ir_2.getValue()>400):
                        #right detected        
                        turning_right=1
                        check_intersection=0
                        turn_time = current_time + 0.66
                                                                                                    
                
                #if leftmost sensor detected blackline we need to check whether it is pure left or has straight line in it
                elif(left_ir_2.getValue()>400):     
                    if((front_ir_left.getValue()>400 or front_ir_right.getValue()>400 or front_ir_mid.getValue()>400)):
                        move_straight=1
                        turn_time = current_time + 0.3
                    #pure left
                    else:
                        turning_left=1
                        check_intersection=0
                        turn_time = current_time + 0.66
                      
       
                
                #following block of code checks for the dead end  
                if(left_ir_1.getValue()<400 and left_ir_2.getValue()<400 and centre_ir.getValue()<400 and right_ir_1.getValue()<400 and right_ir_2.getValue()<400):
                    #dead end detected
                    left_speed = max_speed
                    right_speed = -max_speed
                    dead_end=1
                    rotation_end_time = current_time + 2
            
    
        if(dead_end==1):                
            left_speed = -max_speed * 0.5
            right_speed = max_speed * 0.5
            if(current_time >= rotation_end_time):
                arr=arr+"U"
                dead_end=0 
                
        if(end_maze==0 and turning_right==1): 
                                 
            if(left_ir_2.getValue()>400 and right_ir_2.getValue()>400 and detected==0):
                 turning_left=0
                 print ("T intersection")
                 arr=arr+"R"
                 detected=1
            if((front_ir_left.getValue()>400 or front_ir_right.getValue()>400 or front_ir_mid.getValue()>400) and check_intersection==0):
                print("intersection R and S")
                arr=arr+"R"
            check_intersection=1
            left_speed = max_speed * 1
            right_speed = -max_speed * 0.5
            if(current_time >= turn_time):
                
                turning_right=0
                detected=0
                check_intersection=0
                
                
        if(end_maze==0 and turning_left==1):
            if(left_ir_2.getValue()>400 and right_ir_2.getValue()>400 and detected==0):
                 turning_left=0
                 print ("T intersection")
                 arr=arr+"L"
                 detected=1
            check_intersection=1
            left_speed = -max_speed * 0.5
            right_speed =max_speed * 1
            if(current_time >= turn_time):
                
                turning_left=0
                detected=0
                check_intersection=0
                
        if(move_straight==1):
            left_speed = max_speed * 1
            right_speed =max_speed * 1
            if(current_time >= turn_time):
                move_straight=0
                print("intersection L and S")
                arr=arr+"S"
                check_intersection=0
                
                
        if( front_ir_left.getValue()>400 and front_ir_right.getValue()>400):        
            if(left_ir_2.getValue()>400 or right_ir_2.getValue()>400 ):
                left_speed =0 
                right_speed=0
                end_maze=1 
                turning_right=0
                turning_left=0
                
                
                if write_flag:
                    print (arr)
                    #PATH OF THE FILE IS SAME AS THE PATH OF THE CONTROLLER, CHANGE IT IN THE OPEN LINE TO CHANGE THE LOCATION LIKE D:\\whatever
                    file = open("/home/vivekubuntu/Desktop/path.txt","wt")
                    file.write(arr)
                    file.close()
                    write_flag = False
                    
      
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed) 
        
if __name__ == "__main__":
   
      robot = Robot()
      run_robot(robot)