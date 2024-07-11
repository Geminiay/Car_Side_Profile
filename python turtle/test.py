import turtle
import random
import math

turtle.title("Araç Yan Profili")
s = turtle.getscreen()
t = turtle.Turtle()

taban = 500
yk1 = random.randint(40,60)
arkacam_aci = random.randint(30,60)
arkacam = random.randint(40,60)
tavan = random.randint(100,160)
oncam = random.randint(40,70)
oncam_aci = random.randint(30,90)
kaput = taban-(tavan+(math.cos(math.radians(arkacam_aci))*arkacam)+(math.cos(math.radians(oncam_aci))*oncam)) 
yk2 = yk1+(math.sin(math.radians(arkacam_aci))*arkacam)-(math.sin(math.radians(oncam_aci))*oncam)

print("---------------------------------------Sonuçlar---------------------------------------")
print("Taban Uzunluğu: ",taban,"\t\t\t\tArka Yükseklik: ",yk1,"\nArka Cam Açısı: ",arkacam_aci,"\t\t\t\tArka Cam Uzunluğu: ",arkacam,"\nTavan Uzunluğu: ",tavan,"\nÖn Cam Açısı: ",oncam_aci,"\t\t\t\tÖn Cam Uzunluğu: ",oncam,"\nKaput Uzunluğu: ",kaput,"\t\tÖn Yükseklik: ",yk2)
print("\nArka Cam Cosinüs: ",math.cos(math.radians(arkacam_aci))*arkacam,"\t\t Ön Cam Cosinüs: ",math.cos(math.radians(oncam_aci))*oncam,"\nArka Cam Sinüs: ",math.sin(math.radians(arkacam_aci))*arkacam,"\t\tÖn Cam Sinüs: ",math.sin(math.radians(oncam_aci))*oncam)
print("--------------------------------------------------------------------------------------")

t.fd(taban) 
t.lt(90)
t.fd(yk1)
t.lt(90-arkacam_aci)
t.fd(arkacam)
t.lt(arkacam_aci)
t.fd(tavan)
t.lt(oncam_aci)
t.fd(oncam)
t.rt(oncam_aci)
t.fd(kaput)
t.lt(90)
t.fd(yk2)
t.hideturtle()
turtle.done()



