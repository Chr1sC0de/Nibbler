#include <vector>

template <class _dtype>
class matrix {
    public:
        typedef typename _dtype dtype;
        typedef typename std::vector<dtype> Base;

    public:
        using namespace Base::vector;
};