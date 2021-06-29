n <- 10
inner_color = adjustcolor("darkgreen", alpha.f = 0.75)
outer_color = adjustcolor("black", alpha.f = 0.25)
n_lines <- 40
n_points_per_line <- n_lines * 1.5
min_coord <- -0.05
max_coord <- 1.05

axis_limits = c(-0.1, 1.1)
par(pty = "s", xaxs = "i", yaxs = "i", mar = rep(0, 4))
plot(NA, xlim = axis_limits, ylim = axis_limits, axes = FALSE, ann = FALSE)
for (i in seq_len(n)) {
    x <- matrix(
        rep(seq(0, 1, length.out = n_points_per_line), n_lines),
        ncol = n_lines
    )
    y <- matrix(
        rep(seq(0, 1, length.out = n_lines), n_points_per_line),
        nrow = n_points_per_line,
        byrow = TRUE
    )

    sd <- (x * y + 0.1) / 75
    x <- x + rnorm(length(x), 0, sd)
    y <- y + rnorm(length(y), 0, sd)
    x[x < min_coord] <- min_coord
    x[x > max_coord] <- max_coord
    y <- 1 - y
    y[y < min_coord] <- min_coord
    y[y > max_coord] <- max_coord

    center <- 0.5
    distance_limit <- 2/5
    inner <- sqrt((x - center)**2 + (y - center)**2) <= distance_limit
    outer <- !inner
    x_inner <- x
    x[inner] <- NA
    x_inner[outer] <- NA
    y_inner <- y
    y[inner] <- NA
    y_inner[outer] <- NA

    x_inner <- 1 - x_inner
    y_inner <- 1 - y_inner

    angle <- pi * 3 / 8
    x_inner_centered <- x_inner - center
    y_inner_centered <- y_inner - center
    x_inner <- x_inner_centered * cos(angle) - y_inner_centered * sin(angle) + center
    y_inner <- x_inner_centered * sin(angle) + y_inner_centered * cos(angle) + center

    for (k in seq_len(n_lines)) {
        lines(x[, k], y[, k], col = outer_color)
        lines(x_inner[, k], y_inner[, k], col = inner_color)
    }
}
border_min <- min_coord - 0.04
border_max <- max_coord + 0.04
rect(border_min, border_min, border_max, border_max, lwd = 3)

