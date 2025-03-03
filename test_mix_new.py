# Don't do import *! (It just makes this example smaller)
from pedalboard import *
from pedalboard.io import AudioFile

# Read in a whole file, resampling to our desired sample rate:
samplerate = 44100.0
with AudioFile('ziyouzhanshi.wav').resampled_to(samplerate) as f:
  audio = f.read(f.frames)

# 配置一个“狗叫”效果的吉他踏板链
board = Pedalboard([
    # 使用压缩器来控制动态，使声音更加稳定
    Compressor(threshold_db=-20, ratio=10),

    # 使用低通滤波器（LPF）来模拟狗叫的低频特性
    # LadderFilter(mode=LadderFilter.Mode.LPF12, cutoff_hz=1000),

    # 使用低通滤波器（LPF）来模拟狗叫的低频特性
    LadderFilter(mode=LadderFilter.Mode.LPF12, cutoff_hz=1000),

    # 使用高通滤波器（HPF）来移除极低频的噪声
    HighpassFilter(cutoff_frequency_hz=100),

    # 使用调制效果（如哇音效果）来模拟狗叫的动态变化
    # Wah(wah_range=0.5, rate_hz=1.0),

    # 使用卷积效果器，加载狗叫的音频样本
    Convolution("./woolf.wav", 1.0),
    
    # Convolution("./init.wav", 1.0),

    # 添加一些轻微的延迟效果，增加声音的“回声”感
    # Delay(delay_seconds=0.1, mix=0.3),

    PitchShift(semitones=+12),  # 将音高降低12个半音（一个八度）

    # 使用低频振荡器（LFO）调制音高，模拟狗叫的颤音
    # PitchShift(semitones=4.0),

    # 最后再次调整音量
    Gain(gain_db=30)
])

# Pedalboard objects behave like lists, so you can add plugins:
board.append(Compressor(threshold_db=-25, ratio=10))
board.append(Gain(gain_db=10))
board.append(Limiter())

# ... or change parameters easily:
board[0].threshold_db = -60

# Run the audio through this pedalboard!
effected = board(audio, samplerate)

# Write the audio back as a wav file:
with AudioFile('processed-dog.wav', 'w', samplerate, effected.shape[0]) as f:
  f.write(effected)