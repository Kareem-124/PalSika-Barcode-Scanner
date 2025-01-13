    var element = document.getElementById("total_orders_for_today_value");

    var order_text = element.attributes["data-value"].value;
    order_text = order_text.replace(/'/g, '"'); // switch the ' with " to change it later on to object
    var orders = JSON.parse(order_text); // change the string to object

    var canvas = document.getElementById("canvas_today");
    var ctx = canvas.getContext("2d");

    var colors = ['skyblue', 'gray', 'orange', 'red', 'green'];
    var values = [ orders.pending, orders.work_in_progress, orders.on_hold, orders.canceled,orders.completed]; // Your values
    var labels = ['Voluntary', 'Robot', 'Mandatory']; // Labels for the segments

    dmbChart(75, 75, 50, 10, values, colors, labels);

    function dmbChart(cx, cy, radius, arcwidth, values, colors, labels) {
        var tot = 0;
        var accum = 0;
        var PI = Math.PI;
        var PI2 = PI * 2;
        var offset = -PI / 2;

        ctx.lineWidth = arcwidth;

        // Calculate the total value of all segments
        for (var i = 0; i < values.length; i++) {
            tot += values[i];
        }

        // Draw the donut chart segments
        for (var i = 0; i < values.length; i++) {
            ctx.beginPath();
            ctx.arc(cx, cy, radius,
                offset + PI2 * (accum / tot),
                offset + PI2 * ((accum + values[i]) / tot)
            );
            ctx.strokeStyle = colors[i];
            ctx.stroke();
            accum += values[i];
        }

        // Draw the inner circle to create the donut effect
        var innerRadius = radius - arcwidth - 3;
        ctx.beginPath();
        ctx.arc(cx, cy, innerRadius, 0, PI2);
        ctx.fillStyle = 'white';  // Use white or any other color for the center
        ctx.fill();

        // Show the total value in the center of the donut
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = 'black'; // Text color
        ctx.font = (innerRadius * 0.8) + 'px verdana'; // Font size for total value
        ctx.fillText(tot, cx, cy); // Display the total value in the center

        // Optionally display a label below the total value
        ctx.font = (innerRadius * 0.5) + 'px verdana'; // Font size for label
        ctx.fillText('Order', cx, cy + innerRadius * 0.6); // Display the label 'Total'
    }
