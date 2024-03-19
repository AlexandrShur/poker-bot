from pprint import pprint
from Card import Card
import cv2
import numpy as np

class CardDetector:

    suits_names = ['spades4','diamonds2','clubs8','hearts3']  
    ranks_names = ['eight','nine', 'three','four','six','seven2', 'ace', 'queen', 'ten', 'five', 'two3', 'jack']   

    @classmethod
    def find_suits(self, path, img_gray, img_rgb):
        result = []
        for suit_name in suits_names:
            result = collections.ChainMap(result, self.find_template(path + suit_name + '.png', suit_name, img_gray, img_rgb))

    @classmethod
    def find_samples(self, path, img_gray, img_rgb, samples_names):
        result = {}
        for name in samples_names:
            result = result | self.find_template(path + name + '.png', name, img_gray, img_rgb)
        return result

    @classmethod
    def find_template(self, template_path, template_name, source_img, img_to_draw_rect):
        template = cv2.imread(template_path, 0)  
        w, h = template.shape[::-1]
        result = {}
        res = cv2.matchTemplate(source_img, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.85
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_to_draw_rect, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            if template_name not in result:
                result[template_name] = []
            found_sample = {}
            found_sample["x"] = pt[0]
            found_sample["y"] = pt[1]
            found_sample["height"] = w
            found_sample["width"] = h
            result[template_name].append(found_sample)
            pprint(template_name + ", " + str(pt[0]) + ", " + str(pt[1]))     
        return result

    @classmethod
    def get_cards(self, img_gray, img_rgb):
        suits_dict = self.find_samples('poker/sample/', img_gray, img_rgb, self.suits_names)
        ranks_dict = self.find_samples('poker/sample/', img_gray, img_rgb, self.ranks_names)
        cards = []
        rank_iter = 0
        suit_iter = 0
        for suit_key in suits_dict: 
            for suit in suits_dict[suit_key]:
                suit_iter+=1
                for rank_key in ranks_dict:
                    for rank in ranks_dict[rank_key]:
                        xs = suit['x']
                        xr = rank['x']
                        card_props_threshold = 4
                        diffx = abs(xr - xs)
                        if diffx <= card_props_threshold and diffx >= 0:
                            card = Card()
                            card.name = rank_key + "_" + suit_key
                            card.suit = suit
                            card.rank = rank
                            cards.append(card)
                            pprint(card.name)
        pprint(suit_iter)                    
        return cards
