use pyo3::prelude::*;

/// Define a class "Box" with a position (x,y) and a side (d_left, d_right, d_top, d_bottom)
/// The class has a method "overlap" that returns True if the box overlaps with another box
/// 
///    x-                  x+
/// y+ 
///       ------ top -------
///     left             right
///       ----- bottom -----
/// y-

#[pyclass]
struct Box {
    x0 : f32,
    y0 : f32,
    x: f32,
    y: f32,
    d_left: f32,
    d_right: f32,
    d_top: f32,
    d_bottom: f32,
}

#[pymethods]
impl Box {

    #[new]
    fn new(x0: f32, y0: f32, d_left: f32, d_right: f32, d_top: f32, d_bottom: f32) -> Self {
        let x = x0;
        let y = y0;
        Box { x,y,x0,y0,d_left, d_right, d_top, d_bottom }
    }

    fn width(&self) -> f32 {
        self.d_left + self.d_right
    }

    fn height(&self) -> f32 {
        self.d_top + self.d_bottom
    }

    fn left(&self) -> f32 {
        self.x - self.d_left
    }

    fn right(&self) -> f32 {
        self.x + self.d_right
    }

    fn top(&self) -> f32 {
        self.y + self.d_top
    }

    fn bottom(&self) -> f32 {
        self.y - self.d_bottom
    }

    fn overlap(&self, other: &Box) -> bool {
        if self.right() < other.left()
        {
            return false;
        }
        if self.left() > other.right()
        {
            return false;
        }
        if self.top() < other.bottom()
        {
            return false;
        }
        if self.bottom() > other.top()
        {
            return false;
        }

        return true;

    }

    fn move_towards_origin(&mut self, distance : f32)
    {
        if self.left() > self.x0
        {
            self.x -= distance;
        }
        if self.right() < self.x0
        {
            self.x += distance;
        }
        if self.top() < self.y0
        {
            self.y += distance;
        }
        if self.bottom() > self.y0
        {
            self.y -= distance;
        }

    }

    fn get_overlapping_distance(&self, other: &Box) -> f32 {
        // overlap in x-direction is the minimum of the right side of the first box and the left side of the second box
        let mut overlap_x = other.left() - self.right();
        if overlap_x < 0.0 {
            overlap_x = self.left() - other.right();
        }

        if overlap_x < 0.0 {
            overlap_x = 0.0;
        }

        
        let mut overlap_y = other.top() - self.bottom();
        if overlap_y < 0.0 {
            overlap_y = self.top() - other.bottom();
        }

        if overlap_y < 0.0 {
            overlap_y = 0.0;
        }

        return (overlap_x*overlap_x + overlap_y*overlap_y).sqrt();


    }

    fn line_to_center(&self, other: &Box) -> (f32, f32) {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        return (dx, dy)
    }

    fn distance_to_center(&self, other: &Box) -> f32 {
        let (dx, dy) = self.line_to_center(other);
        return (dx*dx + dy*dy).sqrt();
    }
    
}

#[pyclass]
struct Pusher {
    boxes : Vec<Box>,
    
}

#[pymethods]
impl Pusher {

    #[new]
    fn new() -> Self {
        Pusher { boxes: Vec::new()}
    }

    /// Add a box to the pusher,
    /// returns the index of the newly added box
    
    fn add_box(&mut self, x0: f32, y0: f32, d_left: f32, d_right: f32, d_top: f32, d_bottom: f32) -> usize {
        let new_box = Box::new(x0, y0, d_left, d_right, d_top, d_bottom);
        self.boxes.push(new_box);

        return self.boxes.len() - 1;
    }

    /// Push the boxes so that they don't overlap
    /// returns true if the boxes were pushed
    /// returns false if the boxes don't overlap
    fn push_elements(&mut self, push_factor_horizontal:f32, push_factor_vertical:f32) -> bool{
        let mut push = false;
        for i in 0..self.boxes.len() {
            
            for j in 0..self.boxes.len() {
                if i == j {
                    continue;
                }
                if self.boxes[i].overlap(&self.boxes[j]) {

                    let (mut dx, mut dy) = self.boxes[i].line_to_center(&self.boxes[j]);
                    
                    let overlap = self.boxes[i].get_overlapping_distance(&self.boxes[j]);
                    
                    dx = dx * overlap;
                    dy = dy * overlap;

                    // maximize the move distance to the push factor 
                    // times the size of the box

                    if dx.abs() > push_factor_horizontal * self.boxes[i].width()
                    {
                        dx = dx.signum() * push_factor_horizontal * self.boxes[i].width();
                    }

                    if dy.abs() > push_factor_vertical * self.boxes[i].height()
                    {
                        dy = dy.signum() * push_factor_vertical * self.boxes[i].height();
                    }

                    
                    self.boxes[i].x += dx;
                    self.boxes[i].y += dy;
                    self.boxes[j].x -= dx;
                    self.boxes[j].y -= dy;
                    
                    push = true
                }
            }
        }
        push
    }

    /// Pull all elements towards their original position
    /// if they so not overlap it
    fn pull_elements(&mut self, distance : f32)
    {
        // loop over all boxes
        
        for b in self.boxes.iter_mut()
        {
            b.move_towards_origin(distance);
        }

    }

    /// Get the position of the box
    /// returns the position of the box
    fn get_position(&self, index: usize) -> (f32, f32) {
        (self.boxes[index].x, self.boxes[index].y)
    }

    fn push_free(&mut self, push_factor_horizontal : f32, push_factor_vertical : f32)
        
    {
        if push_factor_horizontal <= 0.0 && push_factor_vertical <= 0.0
        {
            panic!("At least one of the push factors should be larger than 0.0");
        }

        loop {
            let pushed = self.push_elements(push_factor_horizontal, push_factor_vertical);
            if !pushed
            {
                break;
            }
        }
    }
   
}

/// A Python module implemented in Rust.
#[pymodule]
fn nooverlap(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Box>()?;
    m.add_class::<Pusher>()?;
    Ok(())
}
