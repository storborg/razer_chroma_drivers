def linear_fade(start, stop, frames):
    rates = tuple((stop[ch] - start[ch]) / frames for ch in range(3))
    out = []
    for ii in range(frames):
        color = tuple(round(start[ch] + (ii * rates[ch]))
                      for ch in range(3))
        out.append(color)
    return out
