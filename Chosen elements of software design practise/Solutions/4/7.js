const ipToRequestsCount = {};

const lineReader = require('readline').createInterface(require('fs').createReadStream('log.txt'));

lineReader.on('line', line => {
    const ip = line.split(' ')[1];

    if (ipToRequestsCount[ip])
        ipToRequestsCount[ip] += 1;
    else
        ipToRequestsCount[ip] = 1;
});

lineReader.on('close', () => {
    const ips = Object.keys(ipToRequestsCount).sort((a, b) => ipToRequestsCount[b] - ipToRequestsCount[a]).slice(0, 3);

    for (let ip of ips)
        console.log(ip, ipToRequestsCount[ip]);
});