#include <vector>

template <class _dtype>
class matrix {
    public:
        typedef typename _dtype dtype;
        typedef typename std::vector<dtype> Base;
    private:
        std::vector<dtype> data
    public:
        int rows;
        int cols;

        matrix() : rows(0), cols(0) {}
        matrix(int _rows, int _cols): rows(_rows), cols(_cols), data(rows*cols){}

        dtype * operator [] (const int i_row) const {
            return &data[i_row * cols];
        }
        const dtype * operator [] (const int j_col){
            return &data[j_col*cols];
        }
};