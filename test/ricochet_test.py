import math
import numpy as np
import csv
import matplotlib.pyplot as plt


def projectile_ricochet(m_projectile, v_projectile, HV_projectile, HV_armor, angle_of_incidence):

    

    # Calculate the critical energy and angle for ricochet
    angle_of_incidence = math.radians(angle_of_incidence)
    E_critical = ((HV_armor**2)/(16*m_projectile)) * (math.cos(angle_of_incidence))**2
    # Check if the argument of asin is within the domain of [-1, 1]
    sin_argument = math.sqrt(HV_armor/HV_projectile)*math.sin(angle_of_incidence)
    if sin_argument >= 1:
        angle_critical = math.pi/2
    else:
        angle_critical = math.asin(sin_argument)


    projectile_energy = (1/2) * m_projectile * v_projectile**2


    # Check if the projectile has enough energy to ricochet
    if 0 < angle_of_incidence < angle_critical and projectile_energy < E_critical:
        return True
    else:
        return False


if __name__ == '__main__':
    l = []
    x = []
    y = []
    bullet_HV = 50
    for vickers in range(20, 300, 1):
        for projectile_mass in [1]:
            for angle in np.arange(0.1,90,0.1):
                if not projectile_ricochet(projectile_mass, 15, bullet_HV, vickers, angle):

                    s = str(angle)

                    s = s.replace(".", ",")

                    l.append([vickers, s])

                    x.append(vickers)
                    y.append(angle)

                    break

    plt.plot(x, y)
    plt.xlabel('Vickers Hardness of armor')
    plt.ylabel('Maximum angle for ricochet')
    plt.title(f"Energy of bullet: {round(1/2 * 1 * 50**2)}J, Vickers Hardness of projectile: {bullet_HV}")

    plt.show()


    # with open("armor_piercing.csv", 'w', newline='') as file:
    #     writer = csv.writer(file, delimiter=';', dialect="excel",
    #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerows(l)
