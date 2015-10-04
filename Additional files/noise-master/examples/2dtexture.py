"""Writes a 256x256 grayscale simplex noise texture file in pgm format
(see http://netpbm.sourceforge.net/doc/pgm.html)
"""
# $Id: map_generator.py 21 2008-05-21 07:52:29Z casey.duncan $

import sys
import noise
import pygame

filename = 'map.txt'
picname = 'pic.jpeg'
octaves = 5

block_size = 2
width = 512
height = 512
display = (width * block_size, height * block_size)

white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode(display, 0, 32)


f = open(filename, 'wt')

freq = 16.0 * octaves
#f.write('P2\n')
#f.write('256 256\n')
#f.write('255\n')
for y in range(height):
    for x in range(width):
        item = round(noise.snoise3(x / freq, y / freq, 0, octaves=4, persistence=0) * 127.0 + 128.0)
        #item = round(noise.snoise2(x / freq, y / freq, 4) * 127.0 + 128.0)
        #"""
        if item >= 0.5*255:
            item = 255
        else:
            item = 0
            #"""
        screen.fill((item, item, item), (x*block_size, y*block_size, block_size, block_size))
        #f.write("%s" % item)
    f.write('\n')

f.close()

"""
pgm = open(sys.argv[1], 'r').read().split('\n')


x = y = 0

for row in pgm:
    for item in row:
        item = (int(item)/10)*255
        screen.fill((item, item, item), (x, y, block_size, block_size))
        x += block_size
    y += block_size
    x = 0

#screen.blit(surface, (0, 0))

"""

pygame.display.flip()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.image.save(screen, picname)
            print('k')
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

