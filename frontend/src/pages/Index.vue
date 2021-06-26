<template>
  <div class="q-pa-md bg-image">
    <q-page class="flex flex-top ecb-font-bold">
      <div class="full-width full-height row-xs wrap justify-center">
        <div class="col-auto">
          <br>
          <div align="center" class="text-h3 text-white">Let us make your content understandable</div>
        </div>
      </div>
      <div class="fit row wrap justify-center items-start content-start q-gutter-x-md">
        <div class="col-3">
          <q-card style="height: 30vh; width: 24vw">
            <q-card-section>
              <q-avatar icon="double_arrow" color="green" text-color="white"></q-avatar>
              <br>
              <div class="text-h5" align="center">Setting up</div>
              <br>
              <div class="ecb-font-regular text-body2" align="center">Select the topic, summary length and your text
                file you want to summarize
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 30vh; width: 24vw">
            <q-card-section>
              <q-avatar icon="double_arrow" color="secondary" text-color="white"></q-avatar>
              <div class="text-h5" align="center">Summarizing</div>
              <br>
              <div class="ecb-font-regular text-body2" align="center">Run our
                state-of-the-art summarization based on newest NLP algorithms
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-3">
          <q-card style="height: 30vh; width: 24vw">
            <q-card-section>
              <q-avatar icon="double_arrow" color="red" text-color="white"></q-avatar>
              <br>
              <div class="text-h5" align="center">Enjoying</div>
              <br>
              <div class="ecb-font-regular text-body2" align="center">Enjoy the new insights due to complexity reduction
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <div class="fit row wrap justify-center items-start">
        <div class="col-2"></div>
        <div class="col-3 self-center" style="height: 1vh">
          <q-img fit="fill" height="8vh" width="10vw" src="~assets/logo_br_ag.png"/>
        </div>
        <div class="col-3 self-center" style="height: 1vh">
          <q-img fit="fill" height="8vh" width="12vw" src="~assets/logo_senacor.jpg"/>
        </div>
        <div class="col-3 self-center" style="height: 1vh">
          <q-img fit="fill" height="10vh" width="5vw" src="~assets/logo_alexander_thamm.png"/>
        </div>
      </div>
    </q-page>
  </div>
</template>
<style>
.bg-image {
  background-image: url("../assets/background-landing.png");
  width: 100 vv;
  height: 73vh;
  background-repeat: no-repeat;
  background-position: top;;
}
</style>
<script>
export default {
  name: 'PageIndex'
}
</script>
