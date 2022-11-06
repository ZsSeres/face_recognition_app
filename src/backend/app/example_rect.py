from models import BoundingBox

bb1 = BoundingBox(left=10,top=10,right=20,bottom=20)
bb2 = BoundingBox(left=30,top=30,right=40,bottom=40)

print(bb2-bb1)