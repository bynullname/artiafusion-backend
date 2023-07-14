import cv2
import numpy as np
import glob
import os
import urllib.request


class CaseGenerator():
    def __init__(self) -> None:
        self.caseOri = cv2.imread("asserts/case/original/caseOri.png", cv2.IMREAD_UNCHANGED)
        self.caseMask = cv2.imread("asserts/case/original/caseMask.png", cv2.IMREAD_UNCHANGED)
        self.caseMask = self.caseMask.astype(float) / 255

    def read_image_from_url(self, url):
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',  # Do Not Track Request Header
                'Connection': 'keep-alive'
            }
        )
        with urllib.request.urlopen(req) as response:
            arr = np.asarray(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)  # 'Load it as it is'
        return img



    def overlay_image_alpha(self,img, img_overlay, pos, alpha_mask):
        x, y = pos
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])
        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        channels = img.shape[2]
        alpha = 1.0 - alpha_mask[y1o:y2o, x1o:x2o]
        alpha_inv = 1.0 - alpha

        for c in range(channels):
            img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                    alpha_inv * img[y1:y2, x1:x2, c])
    
    def do(self,url):
        skin = self.read_image_from_url(url)
        skin_resized = cv2.resize(skin, (self.caseOri.shape[1], self.caseOri.shape[0]))
        skin_resized = cv2.cvtColor(skin_resized, cv2.COLOR_BGR2BGRA)
        self.overlay_image_alpha(skin_resized,self.caseOri,(0,0),self.caseMask)
        cv2.imwrite('t.png', skin_resized)

if __name__=='__main__':
    cg =CaseGenerator()
    cg.do('https://cdn.midjourney.com/3d049b25-3b7a-4ad1-a50c-88b23fc51f27/0_2.png')
