#!/bin/sh

echo "Hello, World!"

# for i in 0 1 2 3 4
# do
#     echo $i
# done


MyFunction () {
    for i in 0 1 2 3 4
    do
        echo $i
    done
}

StartRosLaunch () {
    roslaunch making_map making_map.launch num_cameras:=$1 camera_angle:=$2 add_shake:=$3 db_id:=$4
}


# MyFunction

# StartRosLaunch 1 0 false 1




# for db in 2 3
# do
#     echo "camera_num:=1 camera_angle:=0 add_shake:=false db_id:=$db"
#     StartRosLaunch 1 0 false $db
#     sleep 10
#     echo "camera_num:=1 camera_angle:=0 add_shake:=true db_id:=$db"
#     StartRosLaunch 1 0 true $db
#     sleep 10
# done


for num in 2 3
do
    for angle in $(seq 0 5 90)
    do
        for db in 1 2 3
        do
            echo "camera_num:=$num camera_angle:=$angle add_shake:=false db_id:=$db"
            StartRosLaunch $num $angle false $db
            sleep 10
            echo "camera_num:=$num camera_angle:=$angle add_shake:=true db_id:=$db"
            StartRosLaunch $num $angle true $db
            sleep 10
        done
    done
done
