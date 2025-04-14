document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    
    if (!fileInput.files.length) {
        alert('Please select a PDF file');
        return;
    }

    const formData = new FormData();
    formData.append('pdf', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Upload failed');
        }

        const data = await response.json();
        
        if (data.concepts && data.concepts.length > 0) {
            visualizeConcepts(data.concepts);
        } else {
            throw new Error('No concepts extracted from the PDF');
        }

    } catch (error) {
        console.error('Upload error:', error);
        alert(error.message);
    }
});


function visualizeConcepts(concepts) {
    const width = 800;
    const height = 600;
    const svg = d3.select('#conceptMap')
        .html('')  // Clear existing content
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2));

    const nodes = concepts.map((concept, index) => ({
        id: index,
        name: concept.name,
        content: concept.content
    }));

    const links = nodes.slice(1).map((node, index) => ({
        source: index,
        target: index + 1
    }));

    const link = svg.append('g')
        .selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('stroke', '#999')
        .attr('stroke-width', 2);

    const node = svg.append('g')
        .selectAll('circle')
        .data(nodes)
        .enter()
        .append('circle')
        .attr('r', 20)
        .attr('fill', '#69b3a2')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    const labels = svg.append('g')
        .selectAll('text')
        .data(nodes)
        .enter()
        .append('text')
        .text(d => d.name.substring(0, 10))
        .attr('font-size', '12px')
        .attr('dx', 15)
        .attr('dy', 4);

    simulation
        .nodes(nodes)
        .on('tick', ticked);

    simulation.force('link')
        .links(links);

    function ticked() {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    }

    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }

    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }

    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }

    // Add click handlers for nodes
    node.on('click', (event, d) => {
        const details = d3.select('.node-details');
        details
            .html(`<h3>${d.name}</h3><p>${d.content}</p>`)
            .style('display', 'block');
    });
}