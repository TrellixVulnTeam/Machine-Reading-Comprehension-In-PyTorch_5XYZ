# -*- coding: utf-8 -*-
# -*- author: JeremySun -*-
# -*- dating: 20/5/18 -*-

# 一个批次中每个句子的词向量均存储在seq_len*word_dim的矩阵中。我们可以借鉴图像处理中的CNN，
# 用一个大小为window_size*word_dim的过滤器依次扫过没连续window_size个词。这样，对于一个文本，
# 一个过滤器可以得出一个长度为(seq_len - window_size + 1)的向量。


import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNMaxPooling(nn.Module):
    def __init__(self, word_dim, window_size, out_channels):  # output_dim表示CNN输出通道数
        super(CNNMaxPooling, self).__init__()
        # 1个输入通道，out_channels个输出通道，过滤器大小为window_size*word_dim
        self.cnn = nn.Conv2d(in_channels=1, out_channels=out_channels, kernel_size=(window_size, word_dim))

    # 输入x为batch组文本，长度为seq_len，词向量长度为word_dim，维度为batch*seq_len*word_dim
    # 输出res为所有文本向量，每个向量的维度为out_channels
    def forward(self, x):
        x_unsqueeze = x.unsqueeze(1)  # 变成单通道，结果维度为batch*1*seq_len*word_dim
        x_cnn = self.cnn(x_unsqueeze)  # CNN，结果维度为batch*out_channels*new_seq_len*1
        x_cnn_result = x_cnn.squeeze(3)  # 删除最后一维，结果维度为batch*out_channels*new_seq_len
        res, _ = x_cnn_result.max(2)  # 最大池化，遍历最后一维求最大值，结果维度为batch*out_channels
        return res


# 测试
batch = 10
seq_len = 20
word_dim = 50
window_size = 3
out_channels = 100

x = torch.randn(batch, seq_len, word_dim)
cnn_max_pooling = CNNMaxPooling(word_dim=word_dim, window_size=window_size, out_channels=out_channels)
res = cnn_max_pooling(x)
print(res.shape)
print(res)

"""
torch.Size([10, 100])
tensor([[0.6062, 0.9637, 0.8716, 0.7029, 1.5214, 1.0372, 0.8889, 1.7713, 0.8723,
         0.9435, 0.9871, 1.4114, 1.1798, 1.3857, 1.4371, 0.7015, 1.0525, 1.1103,
         1.4614, 1.0175, 1.4261, 0.7904, 1.0884, 1.0075, 0.8007, 1.2021, 0.9362,
         0.7817, 0.5340, 1.1235, 0.9365, 0.7916, 0.7245, 1.0243, 1.7593, 0.8591,
         1.0007, 0.5686, 1.2330, 1.6069, 1.0458, 0.6585, 1.0627, 0.6932, 1.2679,
         0.9814, 0.6150, 1.0767, 0.9999, 0.9713, 1.3695, 1.1376, 1.0185, 1.5555,
         1.1945, 1.2155, 1.2840, 0.9873, 1.2371, 1.2428, 1.3522, 1.1845, 1.0975,
         1.0876, 0.9135, 1.5122, 0.9555, 1.0442, 0.8316, 1.3234, 0.9932, 1.4094,
         2.0253, 1.5977, 1.6745, 1.2187, 0.8692, 0.8240, 0.8031, 0.7844, 1.0122,
         0.9474, 1.5301, 0.8650, 1.4003, 0.9403, 0.7107, 0.4808, 1.2415, 0.9344,
         1.7754, 0.9873, 1.2865, 1.0174, 1.5171, 0.7019, 1.0770, 1.6908, 0.7393,
         0.7207],
        [0.9796, 0.7614, 0.7698, 0.6992, 0.7305, 0.9271, 1.0204, 0.9697, 1.4578,
         0.8279, 1.1846, 0.5435, 1.5037, 0.8010, 1.3866, 1.0817, 0.8811, 0.9940,
         0.7494, 1.0652, 1.0977, 1.1503, 1.0114, 1.3036, 0.8244, 1.2384, 1.1321,
         1.1098, 1.4854, 1.1508, 1.4543, 1.4672, 1.1234, 1.0991, 1.2251, 1.0434,
         0.7101, 1.0675, 0.5444, 0.8376, 0.9148, 1.0179, 1.1547, 1.4231, 0.9324,
         0.7320, 0.6903, 0.9727, 0.8217, 0.6805, 0.6734, 0.6562, 1.2828, 1.2942,
         1.6160, 1.6685, 0.8899, 1.1367, 1.0674, 0.7967, 1.0559, 1.0422, 1.4021,
         1.1993, 1.2294, 1.5231, 0.6948, 0.7302, 1.5377, 1.2515, 0.9039, 1.6489,
         1.1923, 1.3075, 0.8265, 1.2704, 1.4305, 1.1285, 0.6662, 0.4570, 1.5798,
         0.6325, 1.0859, 1.7098, 0.9213, 0.8555, 1.1075, 1.0453, 1.1710, 0.6245,
         0.9580, 1.3534, 0.7052, 1.0692, 1.6905, 1.0675, 0.9913, 0.8679, 1.7304,
         0.9989],
        [1.4875, 0.7884, 0.8294, 1.3550, 0.8813, 0.8243, 1.3519, 1.2152, 1.4221,
         0.7705, 1.6593, 0.8323, 1.2620, 0.6449, 0.8580, 0.9186, 0.7325, 1.0167,
         1.0515, 0.6685, 1.4287, 0.9411, 0.9383, 0.6257, 0.8483, 1.0427, 0.8011,
         0.8927, 1.2345, 1.1719, 1.7777, 1.0498, 0.8865, 1.0590, 1.3469, 1.0653,
         0.7643, 0.9376, 0.7653, 0.7181, 0.7785, 1.3451, 1.7344, 1.2459, 1.1906,
         0.7688, 0.8475, 1.2019, 0.8777, 1.2377, 1.6029, 0.6214, 1.5379, 1.3033,
         0.7516, 1.1235, 0.8011, 1.9757, 0.9701, 1.5925, 1.2523, 0.5586, 0.9335,
         1.3980, 1.3174, 1.5391, 0.6178, 1.6029, 0.5994, 1.3985, 1.1296, 1.8660,
         1.2553, 0.9803, 0.5508, 2.1111, 0.6584, 0.6941, 1.1366, 1.1788, 1.1083,
         1.0420, 1.1103, 1.0970, 1.2570, 0.7752, 1.7907, 1.1749, 0.6052, 1.1743,
         0.7636, 0.9909, 0.6085, 0.9552, 0.9963, 0.6236, 0.6000, 1.1047, 1.0391,
         1.1175],
        [1.0854, 0.6256, 0.7976, 0.7083, 1.1888, 0.9033, 1.1511, 0.9691, 1.0529,
         0.9958, 1.3875, 1.4783, 0.9876, 1.1960, 1.3724, 1.1844, 1.2497, 1.2595,
         1.2013, 0.7339, 1.2422, 1.1204, 0.6313, 0.8598, 1.6718, 0.7674, 0.7976,
         1.5221, 0.6612, 1.5513, 1.0364, 0.6458, 0.7886, 1.3887, 0.9520, 0.8086,
         1.0398, 0.8609, 1.7691, 1.5765, 1.2553, 1.7166, 0.7146, 1.5303, 1.4173,
         1.4661, 0.6630, 1.0019, 1.0230, 1.2433, 0.7166, 0.6204, 1.0278, 0.9859,
         0.8368, 0.8438, 1.6472, 1.3592, 1.1012, 1.0277, 1.4346, 1.1976, 0.5734,
         0.8866, 1.0649, 1.0188, 0.4904, 1.0184, 0.8851, 1.7070, 0.6801, 0.9592,
         0.7763, 1.7713, 1.0689, 0.9266, 1.5862, 1.1381, 0.8638, 0.8637, 0.7929,
         0.5957, 0.8750, 0.9811, 1.0902, 0.9261, 1.7654, 1.3629, 1.0351, 1.2454,
         1.0712, 1.4447, 0.6470, 0.8193, 0.3657, 0.3691, 1.0890, 0.9509, 1.3560,
         0.9567],
        [1.1232, 1.2084, 1.1237, 1.1004, 1.3288, 0.7220, 0.8822, 0.7158, 1.5051,
         1.3146, 1.0015, 1.4372, 1.1681, 0.5333, 1.5042, 1.1046, 1.2086, 1.2058,
         1.3501, 0.7078, 0.5298, 0.9760, 0.7658, 0.8056, 1.2043, 0.6727, 0.7766,
         0.7271, 1.1197, 0.9000, 0.8953, 0.5162, 0.8004, 1.2446, 1.6971, 0.8945,
         1.2167, 1.3238, 1.0505, 1.5025, 1.1421, 1.1219, 1.3952, 1.2821, 1.2041,
         0.9276, 0.5673, 1.1665, 1.2206, 1.6221, 1.0397, 1.2191, 1.1148, 1.1943,
         1.2001, 0.8144, 0.4911, 1.7896, 0.8275, 0.7007, 1.1339, 1.0525, 1.2025,
         0.7877, 0.8993, 0.9477, 1.6419, 1.4557, 1.3647, 1.2455, 1.8923, 0.5617,
         0.6012, 1.0966, 0.5242, 1.0385, 0.8337, 1.6816, 1.0288, 0.7004, 1.0597,
         0.6988, 0.8183, 0.9701, 0.8669, 1.1041, 0.8212, 1.2354, 0.7893, 1.0214,
         0.8999, 0.9447, 1.1860, 1.2737, 1.1673, 1.1553, 1.3022, 1.0798, 0.7687,
         1.6020],
        [0.7861, 0.7562, 0.9485, 0.7078, 1.0478, 0.9016, 0.8340, 0.7607, 1.1680,
         1.5799, 0.8991, 1.1551, 1.2707, 0.4865, 1.0848, 1.5501, 0.8472, 1.3306,
         0.8583, 1.0983, 1.2068, 1.3093, 1.0069, 0.8062, 1.1937, 0.8296, 1.5621,
         0.8784, 0.9043, 1.4811, 1.5702, 0.9751, 0.9538, 1.5137, 0.9885, 1.0728,
         0.9280, 2.1094, 1.5574, 1.1137, 1.3695, 0.9536, 0.8793, 1.0731, 1.1180,
         1.2426, 1.7571, 1.1755, 0.6167, 1.0511, 0.8745, 1.3882, 1.2954, 1.1655,
         0.8969, 1.0171, 1.1678, 1.3541, 1.2537, 0.9892, 0.8074, 0.7921, 0.7871,
         1.2971, 1.0037, 1.2603, 0.6834, 1.1384, 0.6206, 0.6902, 1.0108, 0.6378,
         0.8711, 0.9918, 1.2527, 0.5917, 0.4762, 1.3766, 1.0688, 0.9073, 1.2285,
         1.3503, 1.5806, 0.5815, 1.0553, 1.4100, 1.0518, 1.1222, 0.7861, 1.3442,
         1.0977, 0.7310, 1.1604, 0.9007, 0.6727, 0.7240, 0.6990, 1.2129, 0.9407,
         1.1056],
        [1.3768, 0.7495, 1.7092, 0.6568, 1.3920, 2.0760, 1.6067, 1.3900, 1.3352,
         0.9536, 0.8012, 1.3840, 1.7434, 1.3659, 0.8864, 0.9107, 1.0162, 0.6323,
         0.6105, 0.8772, 0.7745, 0.5346, 0.7572, 1.2860, 1.6065, 1.3553, 0.5789,
         0.6107, 0.5732, 0.7486, 0.5192, 0.6825, 1.0036, 0.8449, 1.3033, 1.4074,
         1.1316, 0.8463, 1.4065, 0.8931, 1.0071, 0.6426, 0.5067, 1.2180, 0.7335,
         0.8348, 1.2896, 0.9665, 1.5094, 0.9367, 1.4682, 1.3222, 1.7770, 1.3993,
         0.9150, 1.1803, 1.2000, 0.7744, 0.7601, 0.9464, 1.0557, 0.9700, 1.1334,
         0.8216, 1.1425, 1.2415, 0.9026, 1.3050, 1.5651, 0.9404, 1.1793, 1.3270,
         0.8735, 0.9822, 0.6836, 0.6625, 1.2449, 0.5054, 1.0302, 0.7045, 0.7420,
         1.1067, 0.8516, 0.9067, 0.8052, 1.1811, 1.1867, 0.8584, 1.0886, 0.6335,
         2.1537, 1.0551, 1.2970, 1.0842, 1.6710, 0.8560, 0.6955, 0.6136, 1.1587,
         0.8656],
        [1.0232, 1.0007, 1.1416, 0.7827, 1.0016, 1.2698, 1.1607, 1.3521, 1.0266,
         0.9213, 1.1486, 0.8762, 0.9525, 0.8240, 1.1804, 1.0958, 1.9612, 0.8509,
         1.4136, 0.8624, 1.9393, 1.2471, 0.8675, 0.9247, 0.9161, 0.8194, 1.0494,
         0.7962, 1.1691, 1.0709, 1.2104, 0.9097, 1.1278, 1.2277, 0.7834, 0.7780,
         1.0627, 0.3467, 0.7738, 1.0126, 0.8272, 1.0383, 0.9509, 0.7934, 1.1026,
         1.0749, 1.0133, 1.0961, 0.7736, 0.8450, 1.7228, 1.2605, 0.6479, 0.9737,
         1.1364, 1.0799, 1.1100, 0.6410, 1.1479, 1.1656, 0.9656, 1.5644, 1.2769,
         1.5940, 0.8582, 0.7940, 0.6475, 0.8303, 0.9013, 1.0114, 0.9147, 0.8529,
         0.8802, 0.6687, 0.8738, 1.1524, 1.0190, 0.9224, 1.4331, 1.1747, 0.8880,
         0.7778, 0.7127, 0.9675, 1.3757, 1.2552, 1.2766, 0.9116, 1.1547, 0.8341,
         0.8937, 1.2173, 1.1709, 0.9545, 0.9507, 0.8108, 0.6538, 1.2492, 0.8603,
         0.6957],
        [1.4920, 0.9725, 1.4681, 0.8971, 0.8441, 1.0160, 1.1119, 0.9348, 1.0361,
         0.7369, 0.8053, 0.8450, 0.8841, 1.1825, 1.2208, 1.8013, 0.9845, 1.2131,
         0.7174, 1.0149, 1.0538, 0.8306, 0.9374, 1.0395, 1.1358, 2.1123, 0.6030,
         0.9078, 1.8527, 1.8416, 1.3403, 2.0257, 0.9649, 1.4605, 1.9540, 0.8489,
         0.7739, 0.9133, 1.0625, 0.8357, 1.0779, 0.8210, 1.2570, 1.4002, 0.9771,
         0.9506, 1.1385, 0.8681, 1.4274, 1.0223, 1.7831, 1.1244, 0.6854, 1.0654,
         1.6641, 1.6621, 0.7446, 0.5670, 0.9855, 0.8686, 1.4191, 0.8291, 0.9781,
         1.0628, 0.8828, 1.1299, 1.3145, 0.9753, 1.2491, 0.9022, 1.1707, 0.6894,
         0.8338, 0.9924, 1.5113, 1.0742, 0.8957, 1.0485, 1.6114, 0.7970, 1.9532,
         0.6008, 0.9055, 1.5196, 1.5719, 1.1319, 0.8470, 1.2732, 0.8641, 0.7816,
         0.8492, 0.7278, 1.1012, 1.3317, 0.8225, 1.1343, 0.7704, 1.2477, 0.9540,
         0.9055],
        [1.6531, 1.2123, 1.0785, 0.6515, 0.9740, 0.5604, 0.8596, 1.3548, 0.7466,
         0.5813, 1.0681, 1.0525, 1.3025, 0.7098, 0.9982, 0.9380, 0.9237, 0.7845,
         0.4932, 1.0720, 1.3429, 1.3530, 0.7400, 0.7898, 1.7220, 0.9068, 1.0827,
         0.8057, 0.8250, 1.2385, 1.0253, 0.8721, 0.7426, 0.9132, 1.0242, 0.7442,
         0.8377, 0.7946, 0.7020, 1.0844, 0.6833, 1.1241, 0.6502, 1.1791, 0.8702,
         0.7500, 1.2491, 1.4986, 0.8883, 0.8821, 0.8220, 0.7481, 1.0914, 1.4431,
         1.2814, 1.1149, 0.9602, 0.8754, 0.8618, 0.8486, 0.9307, 0.6441, 1.1085,
         1.1242, 1.6341, 1.0923, 1.0899, 0.6520, 0.5848, 1.1754, 0.8720, 0.9313,
         1.2830, 1.5017, 1.2892, 0.8303, 0.3792, 1.4600, 0.8992, 0.9396, 1.6627,
         0.8033, 1.1622, 0.8097, 0.7542, 0.9122, 0.7110, 0.9841, 0.6626, 0.8811,
         1.0548, 1.2600, 0.8230, 1.0768, 1.2928, 0.7417, 0.7271, 1.0255, 0.9194,
         1.1010]], grad_fn=<MaxBackward0>)
"""
