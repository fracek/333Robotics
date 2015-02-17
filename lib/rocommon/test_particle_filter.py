import particles
import numpy as np

if __name__ == "__main__":
    n = 20
    particles = particles.ParticleSet([0, 0, 0], n, e_sigma=0.03, f_sigma=0.01, g_sigma=0.03)
    particles.x[0] = [1, 2, 3]
    particles.x[10] = [9, 9, 9]
    particles.w[0] = 0.8
    particles.w[10] = 0.4
    particles.normalize()
    print particles.w
    particles.resample()
    print particles.x
    print particles.w
    
    # first and third row should be relatively similar, second row about half of either one
    print 'Stats'
    print (particles.x == [1, 2, 3]).sum() / 3
    print (particles.x == [9, 9, 9]).sum() / 3
    print (particles.x == [0, 0, 0]).sum() / 3
