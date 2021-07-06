<template>
  <div class="q-pa-md bg-image">
    <q-page class="flex flex-top ecb-font-bold">
      <div class="full-width full-height row-xs justify-center">
        <div class="col-auto">
          <br>
          <div align="center" class="text-h3 text-white">Making content accessible...</div>
        </div>
      </div>
      <div class="fit row wrap justify-center items-stretch content-start q-gutter-x-lg">
        <div class="col-2 items-stretch">
          <q-card>
            <q-card-section>
              <q-avatar color="green" icon="double_arrow" size="sm" text-color="white"></q-avatar>
              <br>
              <div align="center" class="text-h5">Setting up</div>
              <br>
              <div align="center" class="ecb-font-regular text-body2">Select the topic, summary length and your text
                file you want to summarise
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-2 items-stretch">
          <q-card>
            <q-card-section>
              <q-avatar color="secondary" icon="double_arrow" size="sm" text-color="white"></q-avatar>
              <div align="center" class="text-h5">Summarising</div>
              <br>
              <div align="center" class="ecb-font-regular text-body2">Run our
                state-of-the-art summarisation based on newest NLP algorithms
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-2 items-stretch">
          <q-card>
            <q-card-section>
              <q-avatar color="red" icon="double_arrow" size="sm" text-color="white"></q-avatar>
              <br>
              <div align="center" class="text-h5">Enjoying</div>
              <br>
              <div align="center" class="ecb-font-regular text-body2">Gain insight into the distilled content
                <br/><br/></div>
            </q-card-section>
          </q-card>
        </div>
      </div>
      <div class="fit row wrap justify-center items-stretch content-start q-gutter-x-lg">
        <div class="col-2"></div>
        <div class="col-1 self-center content-center justify-center">
          <q-img src="~assets/logo_br_ag.png" fit="scale-down"/>
        </div>
        <div class="col-1"></div>
        <div class="col-1 self-center content-center justify-center">
          <q-img src="~assets/logo_senacor.jpg" fit="scale-down"/>
        </div>
        <div class="col-1"></div>
        <div class="col-1 self-center content-center justify-center">
          <q-img src="~assets/logo_alexander_thamm.png" height="50px" width="50px" fit="scale-down"/>
        </div>
        <div class="col-2"></div>
      </div>
    </q-page>
  </div>
</template>
<style>
.bg-image {
  background-image: url("../assets/background-landing.png");
  width: 100vw;
  height: 69vh;
  background-repeat: no-repeat;
  background-position: top;
}
</style>
<script>
export default {
  name: 'PageIndex'
}
</script>
