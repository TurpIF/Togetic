#ifndef TOGETIC_KINECT_H
#define TOGETIC_KINECT_H

#include "NiTE.h"

#define MAX_DEPTH 10000

class Kinect {
  public:
    Kinect(const char* strSampleName, float * x, float * y, float * z);
    virtual ~Kinect();

    virtual openni::Status Init(int argc, char **argv);
    virtual openni::Status Run();
    void Update();

  protected:
    void Finalize();

  private:
    Kinect(const Kinect&);
    Kinect& operator=(Kinect&);
    void UpdateXYZ(nite::UserTracker* pUserTracker, const
        nite::UserData& userData);

    static Kinect* ms_self;

    float m_pDepthHist[MAX_DEPTH];
    char m_strSampleName[ONI_MAX_STR];
    openni::RGB888Pixel* m_pTexMap;
    unsigned int m_nTexMapX;
    unsigned int m_nTexMapY;
    openni::Device m_device;
    nite::UserTracker* m_pUserTracker;
    nite::UserId m_poseUser;
    uint64_t m_poseTime;
    float * m_x;
    float * m_y;
    float * m_z;
};

#endif // TOGETIC_KINECT_H

