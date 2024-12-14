# utility.py
import math

def check_collision(obj1, obj2):
    """ตรวจสอบว่ามีการชนกันระหว่าง obj1 และ obj2 หรือไม่"""
    distance = math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)
    return distance < (obj1.size + obj2.size)
