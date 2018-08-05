from matplotlib import pyplot as plt


def oscillator(damping):
    damping = float(damping)
    weight  =  1.0
    value   =  0.0
    middle  = value

    yield value

    while(1):
        if(value<middle):
            weight+=damping
        else:
            weight-=damping

        value+=weight

        yield value

the_generator = oscillator(.1)
list_of_generated_values = []
for i in range(100):
    list_of_generated_values.append(the_generator.next())


plt.plot(list_of_generated_values)
plt.show()


