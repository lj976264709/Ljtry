function centriod_num=marked_watershed(picturefile,a)%图片路径，腐蚀膨胀系数
%%
%步骤一：读取彩色图像并转化为灰度图
I = imread(picturefile);

%%
%******************步骤二：基于重建的开闭操作************************************

se = strel('disk',a);%disk指定构建一个圆形的结构体，第二个参数指定结构体的半径

%接下来，进行基于重建的开操作。使用imerode和imreconstruct函数实现
Ie = imerode(I, se);%先腐蚀‘erosion’
Iobr = imreconstruct(Ie, I);%再重建

Iobrd = imdilate(Iobr, se);%在基于重建的开操作的结果基础上，进行腐蚀
Iobrcbr = imreconstruct(imcomplement(Iobrd), imcomplement(Iobr));%重建，标记图像为腐蚀后图像取补，模板为腐蚀前原图取补。
Iobrcbr = imcomplement(Iobrcbr);%重建结果再取补，得到实际基于重建的闭操作的结果。
%figure
%imshow(Iobrcbr), title('基于重建的开+闭操作 (Iobrcbr)')


%%
%******************步骤三：标记前景物体************************************
%计算Iobrcbr的区域极大值来得到好的前景标记。
%得到的前景标记图fgm是二值图，白色对应前景区域
fgm = imregionalmax(Iobrcbr);

%为了方便解释结果，将前景标记图叠加到原始图像上
I2 = I;
I2(fgm) = 255;%将fgm中的前景区域（像素值为1）标记到原图上（置白色）

%注意到一些大部分重合或被阴影遮挡的物体没有被标记出来。这意味着这些物体最终可能不会被正确的分割出来。
%并且，有些物体中前景标记正确的到达了物体的边缘。这意味着你应该清除掉标记斑块的边缘，向内收缩一点。
%你可以通过先闭操作，再腐蚀做到这点。
se2 = strel(ones(2,2));
fgm2 = imclose(fgm, se2);
fgm3 = imerode(fgm2, se2);

%这个操作会导致遗留下一些离群的孤立点，这些是需要被移除的。
%你可以通过bwareaopen做到这点，函数将移除那些包含像素点个数少于指定值的区域。
fgm4 = bwareaopen(fgm3, 2);
I3 = I;
I3(fgm4) = 255;

%%
%*********************第四步：计算背景标记**********************************
%本例中设计出的标记背景算法的前提假设是：图像中相对亮的是物体，相对暗的区域是背景。
%如果不满足这条假设，标记结果可能不甚理想

%现在你需要标记背景。在去除噪点后的图像Iobrcbr中，暗像素属于背景，所以你可以先进行一下阈值操作。
%bw = imbinarize(Iobrcbr);
bw=im2bw(Iobrcbr,graythresh(Iobrcbr));%我使用上一行代码报错了，故换了一种二值化方法

%背景像素现在是黑的了，但是理想情况下我们不希望背景标记太接近我们想要分割的物体的边界。

D = bwdist(bw);
%D = bwdist(BW)计算二值图像BW的欧几里得矩阵。对BW的每一个像素，距离变换指定像素和最近的BW非零像素的距离。
%bwdist默认使用欧几里得距离公式。BW可以由任意维数，D与BW有同样的大小。

%由于bw中目标物体是白色的1.所以D中对应的目标物体处均是0，随着进入背景越深，对应像素值越大。
%这时正好符合我们使用分水岭算法的假设（想分出的目标物体数值较低）
%于是得到的背景标记是 物体与背景间的一个圈，能够包住目标物体
DL = watershed(D);
bgm = DL == 0;%分水岭变换结果L中，同一区域用同一数字表示，区域间分界线同一由0标识

%%
%******************第五步：计算分割函数（修改后）的分水岭变换*****************
% 函数imimposemin可以被用来修改一副图片，使得其只在指定的位置处取得局部最小值
% 这里你可以使用imimposemin来修改梯度幅值图像，使得局部最小值只出现在前景标记和背景标记处。
% 从结果来看imimposemin会将指定区域置为-Inf，从而成为极小值
% 且图像变得相当“平整”，一块块的相同数值的区域


%使用Sobel边缘检测算子，imfilter函数，和一些简单的四则运算来计算梯度幅值。
%梯度值总是在物体的边缘处高，而总是在物体内部低。
hy = fspecial('sobel');%获取sobel算子模板，计算纵向梯度
hx = hy';%横向模板
Iy = imfilter(double(I), hy, 'replicate');%计算纵向梯度
Ix = imfilter(double(I), hx, 'replicate');
gradmag = sqrt(Ix.^2 + Iy.^2);%计算梯度幅值

gradmag2 = imimposemin(gradmag, bgm | fgm4);

%Finally we are ready to compute the watershed-based segmentation.
L = watershed(gradmag2);
%%
L=rgb2gray(L);%大菠萝悄悄加上去的
[L,num] = bwlabel(L,4);%对边缘进行标记,L将不同连通域进行标记，num表示连通域的个数

for i=1:num%将各个连通域的质心输出到数组中
    stats = regionprops(L ==i, 'all');
    centriods= stats.Centroid;
    centriod_num(i,1)=centriods(1);
    centriod_num(i,2)=centriods(2);
end