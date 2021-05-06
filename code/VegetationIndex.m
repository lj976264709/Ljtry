function centriod_num=vegetationindex(picturefile,url)
image = imread(picturefile);
centriod_num=[];

image_double = double(image);
%imshow(image);
R = image_double(:,:,1);
G = image_double(:,:,2);
B = image_double(:,:,3);
%x=G-R;
%y=G+R;
%归一化绿-红差值指数（NGRDI）
NGRDI = (G - R) ./ (G + R);
imshow(NGRDI);
% imwrite(NGRDI,'D:\yjs\img\lanqiuchang_NGRDI.png');
%进行otsu阈值分割，对图像进行二值化处理，并合成彩色图像，实现根据前后景的区分，即完成植被与其他地类的区分。

NGRDI_level = graythresh(G);
NGRDI_bw = im2bw(NGRDI,NGRDI_level);
imshow(NGRDI_bw);
%imwrite(NGRDI_bw,'D:\shaoxing_test2_rgb_bw.tif')
NGRDI_bw1 = imcomplement(NGRDI_bw);
imshow(NGRDI_bw1);
NGRDI_bw_R = R .* NGRDI_bw;
NGRDI_bw_G = G .* NGRDI_bw;
NGRDI_bw_B = B .* NGRDI_bw;
NGRDI_bw = cat(3, NGRDI_bw_R, NGRDI_bw_G, NGRDI_bw_B);
NGRDI_rgb = uint8(NGRDI_bw);
%imshow(NGRDI_rgb)
%imwrite(NGRDI_rgb,'D:\yangshu_test1_rgb.tif');
image=rgb2gray(NGRDI_rgb);
imagenew=imbinarize(image);
%imshow(imagenew)

%过绿指数（ExG）
R1 = R / 255;
G1 = G / 255;
B1 = B / 255;
r1 = R1 ./ (R1 + B1 + G1);
g1 = G1 ./ (R1 + B1 + G1);
b1 = B1 ./ (R1 + B1 + G1);
exg = 2 * g1 - r1 - b1;
%imshow(exg)

%imwrite(exg,'D:\yjs\img\Google3_exg.PNG');

exg_level = graythresh(exg);
exg_bw = im2bw(exg,exg_level);
exg_bw_R = R .* exg_bw;
exg_bw_G = G .* exg_bw;
exg_bw_B = B .* exg_bw;
exg_bw = cat(3, exg_bw_R, exg_bw_G, exg_bw_B);
exg_rgb = uint8(exg_bw);

%imshow(exg_rgb)
%imwrite(exg_rgb,'D:\exg.tif');
% 
% 
% 
% 
% 
% 
% %过绿减过红指数（ExG-ExR）
exr = 1.4 * r1 - g1;
exgr = exg - exr;
%imwrite(exgr,'D:\2_1_916_exg-exr.png');

exgr_level = graythresh(exgr);
exgr_bw = im2bw(exgr,exgr_level);
exgr_bw_R = R .* exgr_bw;
exgr_bw_G = G .* exgr_bw;
exgr_bw_B = B .* exgr_bw;
exgr_bw = cat(3, exgr_bw_R, exgr_bw_G, exgr_bw_B);
exgr_rgb = uint8(exgr_bw);
%imshow(exgr_rgb)
%imwrite(exgr_rgb,'D:\exgr_rgb.tif');
% 
% 
% %绿叶指数（GLI）
GLI = (2 * G - R - B)./(2 * G + R + B);
imwrite(GLI,url);

GLI_level = graythresh(GLI);
GLI_bw = im2bw(GLI,GLI_level);
GLI_bw_R = R .* GLI_bw;
GLI_bw_G = G .* GLI_bw;
GLI_bw_B = B .* GLI_bw;
GLI_bw = cat(3, GLI_bw_R, GLI_bw_G, GLI_bw_B);
GLI_rgb = uint8(GLI_bw);
%imshow(GLI_rgb)
%imwrite(GLI_rgb,'D:\GLI_rgb.tif');

subplot(221);imshow(image);title('image');
subplot(222);imshow(NGRDI);title('NGRDI');
subplot(223);imshow(exg);title('ExG');
subplot(224);imshow(exgr);title('GLI_rgb');

