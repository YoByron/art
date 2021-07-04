coord_max <- 1
coord_padding <- 0.05
coord_limit <- coord_max + coord_padding
border_limit <- coord_limit + 0.05
axis_limits = c(-border_limit - 0.05, border_limit + 0.05)
n <- 100
rnorm_sd <- 0.01
coordinates <- complex(
    real = rep(seq(-coord_max, coord_max, length.out = n), n),
    imaginary = rep(seq(coord_max, -coord_max, length.out = n), each = n)
)
coordinates <- matrix(coordinates, nrow = n, byrow = TRUE)
coordinates <- coordinates +
    rnorm(length(coordinates), 0, rnorm_sd) +     # noise in x
    rnorm(length(coordinates), 0, rnorm_sd) * 1i  # noise in y
# coordinates

disk_mask <- abs(coordinates) < 2/3
disk_inner <- coordinates
disk_inner[!disk_mask] <- NA
disk_outer <- coordinates
disk_outer[disk_mask] <- NA

# rotate the inner lines
angle <- pi * 3 / 8
disk_inner <- disk_inner * complex(real = cos(angle), imaginary = sin(angle))


par(pty = "s", xaxs = "i", yaxs = "i", mar = rep(0, 4))
plot(NA, xlim = axis_limits, ylim = axis_limits, axes = FALSE, ann = FALSE)
rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "#f0f0f0", border = NA)
for (i in seq_len(n)) {
    lines(disk_outer[i, ])
    lines(disk_inner[i, ], col = "darkgreen")
}
