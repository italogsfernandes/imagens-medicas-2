$(document).ready(function() {
  $(id_btn_do_something).click(function() {
    console.log("hello there");
    // Random tree
    const N = 300;
    const gData = {
      nodes: [...Array(N).keys()].map(i => ({ id: i })),
      links: [...Array(N).keys()]
        .filter(id => id)
        .map(id => ({
          source: id,
          target: Math.round(Math.random() * (id-1))
        }))
    };
    const Graph = ForceGraph3D()
      (document.getElementById('3d-graph'))
        .graphData(gData);

  });
});
