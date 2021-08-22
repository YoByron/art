n <- 10
inner_color = adjustcolor("darkgreen", alpha.f = 0.75)
outer_color = adjustcolor("black", alpha.f = 0.2)
n_lines <- 40
n_points_per_line <- ceiling(n_lines * 1.5)
coord_max <- 0.5
coord_padding <- 0.05
coord_limit <- coord_max + coord_padding
border_limit <- coord_limit + 0.05
axis_limits = c(-border_limit - 0.05, border_limit + 0.05)

par(pty = "s", xaxs = "i", yaxs = "i", mar = rep(0, 4))
plot(NA, xlim = axis_limits, ylim = axis_limits, axes = FALSE, ann = FALSE)
for (i in seq_len(n)) {
    x <- matrix(
        rep(seq(-coord_max, coord_max, length.out = n_points_per_line), n_lines),
        ncol = n_lines
    )
    y <- matrix(rep(seq(-coord_max, coord_max, length.out = n_lines), n_points_per_line),
        nrow = n_points_per_line,
        byrow = TRUE
    )

    sd <- ((x + coord_max) * (y + coord_max) + 0.1) / 75
    x <- x + rnorm(length(x), 0, sd)
    y <- y + rnorm(length(y), 0, sd)
    x[x < -coord_limit] <- -coord_limit
    x[x > coord_limit] <- coord_limit
    y <- -y
    y[y < -coord_limit] <- coord_limit
    y[y > coord_limit] <- coord_limit

    distance_limit <- 0.39
    inner <- sqrt(x*x + y*y) <= distance_limit
    outer <- !inner
    x_inner <- x
    x[inner] <- NA
    x_inner[outer] <- NA
    y_inner <- y
    y[inner] <- NA
    y_inner[outer] <- NA

    x_inner <- -x_inner
    # y_inner <- -y_inner

    angle <- pi * 3 / 8
    x_inner_rotated <- x_inner * cos(angle) - y_inner * sin(angle)
    y_inner_rotated <- x_inner * sin(angle) + y_inner * cos(angle)

    for (k in seq_len(n_lines)) {
        lines(x[, k], y[, k], col = outer_color)
        lines(x_inner_rotated[, k], y_inner_rotated[, k], col = inner_color)
    }
}
rect(-border_limit, -border_limit, border_limit, border_limit, lwd = 3)
