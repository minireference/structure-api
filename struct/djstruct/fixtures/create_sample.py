
n1 = BaseNode(path='math/quadratic_equation')
n1.save()
n2 = BaseNode(path='mechanics/kinematics')
n2.save()
n3 = BaseNode(path='mechanics/projectile_motion')
n3.save()


r12 = DependencyRelation(
        prerequisite=n1,
        usedfor=n2,
        level='UGRAD',
        explain_usedfor='Solving quadratics is useful in kinematics.', 
        explain_prerequisite='You need to know how to solve quadratic equations to solve certain kinematics problems.'
)
r12.save()
r23 = DependencyRelation(
        prerequisite=n2,
        usedfor=n3,
        level='UGRAD',
        explain_usedfor='One-dimensional kinematics is used in two-dimensional projectile motion.', 
        explain_prerequisite='You should be familiar with one-dimensional kinamtics before attacking two-dimensional kinematics porblems.'
)
r23.save()